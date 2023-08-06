/*
 * Copyright (C) 2019 Istituto Italiano di Tecnologia (IIT)
 * All rights reserved.
 *
 * This software may be modified and distributed under the terms of the
 * GNU Lesser General Public License v2.1 or any later version.
 */

#include "gympp/gazebo/GymFactory.h"
#include "gympp/base/Log.h"
#include "gympp/base/Space.h"
#include "gympp/gazebo/GazeboEnvironment.h"
#include "gympp/gazebo/Metadata.h"
#include "scenario/gazebo/GazeboSimulator.h"
#include "scenario/gazebo/utils.h"

#include <cassert>
#include <ostream>
#include <unordered_map>

using namespace gympp::base;
using namespace gympp::gazebo;

class GymFactory::Impl
{
public:
    inline bool exists(const EnvironmentName& name) const
    {
        return plugins.find(name) != plugins.end();
    }

    spaces::SpacePtr makeSpace(const SpaceMetadata& md);
    std::unordered_map<EnvironmentName, const PluginMetadata> plugins;
};

GymFactory::GymFactory()
    : pImpl{new Impl()}
{}

GymFactory::~GymFactory() = default;

bool GymFactory::registerPlugin(const PluginMetadata& md)
{
    if (!md.isValid()) {
        gymppError << "The plugin metadata is not valid" << std::endl;
        return false;
    }

    if (pImpl->exists(md.environmentName)) {
        gymppWarning
            << "Environment '" << md.environmentName
            << "' has been already registered. This operation will be no-op."
            << std::endl;
        return true;
    }

    pImpl->plugins.insert({md.environmentName, md});
    return true;
}

gympp::base::EnvironmentPtr GymFactory::make(const std::string& envName)
{
    if (!pImpl->exists(envName)) {
        gymppError << "Environment '" << envName
                   << "' has never been registered" << std::endl;
        return nullptr;
    }

    auto& md = pImpl->plugins[envName];

    assert(md.isValid());
    auto actionSpace = pImpl->makeSpace(md.actionSpace);
    auto observationSpace = pImpl->makeSpace(md.observationSpace);

    if (!actionSpace || !observationSpace) {
        gymppError << "Failed to create spaces" << std::endl;
        return nullptr;
    }

    // Create the environment
    auto ignGym = std::make_shared<gazebo::GazeboEnvironment>(
        actionSpace,
        observationSpace,
        md.agentRate,
        md.getPhysicsData().rtf,
        1 / md.getPhysicsData().maxStepSize);

    // Find the file if it is not an absolute path
    std::string worldFile =
        scenario::gazebo::utils::findSdfFile(md.worldFileName);

    if (worldFile.empty()) {
        return nullptr;
    }

    // Insert the world
    if (!ignGym->insertWorldFromSDF(worldFile)) {
        gymppError << "Failed to insert an empty world" << std::endl;
        return nullptr;
    }

    // Create the model initialization data
    ModelInitData modelData;
    modelData.modelFile = md.getModelFileName();
    // TODO: expose position and orientation?

    // Store the model data in the environment
    ignGym->storeModelData(modelData);

    // Create the gympp plugin data
    PluginData pluginData;
    pluginData.libName = md.libraryName;
    pluginData.className = md.className;

    // Store the gympp plugin data
    ignGym->storePluginData(pluginData);

    // Return the pointer to the gympp::Environment interface
    return ignGym->env();
}

gympp::base::spaces::SpacePtr
GymFactory::Impl::makeSpace(const SpaceMetadata& md)
{
    assert(md.isValid());
    gympp::base::spaces::SpacePtr space;

    switch (md.type) {
        case gympp::gazebo::SpaceType::Box: {
            if (md.dims.empty()) {
                space =
                    std::make_shared<gympp::base::spaces::Box>(md.low, md.high);
            }
            else {
                space = std::make_shared<gympp::base::spaces::Box>(
                    md.low[0], md.high[0], md.dims);
            }
            break;
        }
        case gympp::gazebo::SpaceType::Discrete: {
            space = std::make_shared<gympp::base::spaces::Discrete>(md.dims[0]);
            break;
        }
    }

    return space;
}
