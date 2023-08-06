/*
 * Copyright (C) 2019 Istituto Italiano di Tecnologia (IIT)
 * All rights reserved.
 *
 * This software may be modified and distributed under the terms of the
 * GNU Lesser General Public License v2.1 or any later version.
 */

#ifndef GYMPP_GAZEBO_METADATA
#define GYMPP_GAZEBO_METADATA

#include "gympp/base/Log.h"
#include "gympp/base/Space.h"
#include "scenario/gazebo/GazeboSimulator.h"

#include <string>
#include <vector>

namespace gympp {
    namespace gazebo {
        class GymFactory;
        class SpaceMetadata;
        class PluginMetadata;

        struct PluginData;
        struct PhysicsData;
        struct ModelInitData;

        enum class SpaceType
        {
            Discrete,
            Box
        };
    } // namespace gazebo
} // namespace gympp

struct gympp::gazebo::PluginData
{
    std::string libName;
    std::string className;
};

struct gympp::gazebo::ModelInitData
{
    std::string modelFile;
    bool fixedPose = false;
    std::string baseLink = "";
    std::string modelName = "";
    std::array<double, 3> position = {0, 0, 0};
    std::array<double, 4> orientation = {1, 0, 0, 0};
};

struct gympp::gazebo::PhysicsData
{
    double rtf;
    double maxStepSize;
    const double realTimeUpdateRate = -1;

    PhysicsData(double _rtf = 1, double _maxStepSize = 0.001)
        : rtf(_rtf)
        , maxStepSize(_maxStepSize)
    {}

    PhysicsData(const PhysicsData& other)
        : rtf(other.rtf)
        , maxStepSize(other.maxStepSize)
        , realTimeUpdateRate(other.realTimeUpdateRate)
    {}

    PhysicsData& operator=(const PhysicsData& other)
    {
        rtf = other.rtf;
        maxStepSize = other.maxStepSize;
        return *this;
    }

    bool operator==(const PhysicsData& other)
    {
        return other.rtf == rtf && other.maxStepSize == maxStepSize
               && other.realTimeUpdateRate == realTimeUpdateRate;
    }
};

class gympp::gazebo::SpaceMetadata
{
private:
    friend gympp::gazebo::GymFactory;

    SpaceType type;
    std::vector<size_t> dims;

    gympp::base::spaces::Box::Limit low;
    gympp::base::spaces::Box::Limit high;

    bool boxSpaceValid() const
    {
        if (low.size() != high.size()) {
            gymppError << "The size of the limits do not match" << std::endl;
            return false;
        }

        if (dims.empty()) {
            if (low.empty()) {
                gymppError << "The limits do not contain any data" << std::endl;
                return false;
            }
        }
        else {
            if (low.size() != 1) {
                gymppError << "The limits must be scalar values" << std::endl;
                return false;
            }
        }

        return true;
    }

    bool discreteSpaceValid() const
    {
        if (dims.size() != 1 && dims[0] <= 0) {
            return false;
        }

        return true;
    }

public:
    inline SpaceType getType() const { return type; }
    inline std::vector<size_t> getDimensions() const { return dims; }
    inline gympp::base::spaces::Box::Limit getLowLimit() const { return low; }
    inline gympp::base::spaces::Box::Limit getHighLimit() const { return high; }

    inline void setType(const SpaceType type) { this->type = type; }
    inline void setDimensions(const std::vector<size_t>& dims)
    {
        this->dims = dims;
    }
    inline void setLowLimit(const gympp::base::spaces::Box::Limit& limit)
    {
        this->low = limit;
    }
    inline void setHighLimit(const gympp::base::spaces::Box::Limit& limit)
    {
        this->high = limit;
    }

    bool isValid() const
    {
        switch (type) {
            case SpaceType::Box:
                return boxSpaceValid();
            case SpaceType::Discrete:
                return discreteSpaceValid();
        }

        return true;
    }
};

class gympp::gazebo::PluginMetadata
{
private:
    friend gympp::gazebo::GymFactory;
    std::string environmentName;
    std::string libraryName;
    std::string className;

    std::string modelFileName;
    std::string worldFileName;

    double agentRate;
    PhysicsData physicsData;

    SpaceMetadata actionSpace;
    SpaceMetadata observationSpace;

public:
    inline std::string getEnvironmentName() const { return environmentName; }
    inline std::string getLibraryName() const { return libraryName; }
    inline std::string getClassName() const { return className; }
    inline std::string getModelFileName() const { return modelFileName; }
    inline std::string getWorldFileName() const { return worldFileName; }
    inline double getAgentRate() const { return agentRate; }
    inline PhysicsData getPhysicsData() const { return physicsData; }
    inline SpaceMetadata getActionSpaceMetadata() const { return actionSpace; }
    inline SpaceMetadata getObservationSpaceMetadata() const
    {
        return observationSpace;
    }

    inline void setEnvironmentName(const std::string& environmentName)
    {
        this->environmentName = environmentName;
    }

    inline void setActionSpaceMetadata(const SpaceMetadata& actionSpaceMetadata)
    {
        this->actionSpace = actionSpaceMetadata;
    }

    inline void
    setObservationSpaceMetadata(const SpaceMetadata& observationSpaceMetadata)
    {
        this->observationSpace = observationSpaceMetadata;
    }

    inline void setLibraryName(const std::string& libraryName)
    {
        this->libraryName = libraryName;
    }
    inline void setClassName(const std::string& className)
    {
        this->className = className;
    }
    inline void setModelFileName(const std::string& modelFileName)
    {
        this->modelFileName = modelFileName;
    }
    inline void setWorldFileName(const std::string& worldFileName)
    {
        this->worldFileName = worldFileName;
    }

    inline void setAgentRate(const double agentRate)
    {
        this->agentRate = agentRate;
    }

    inline void setPhysicsData(const PhysicsData& physicsData)
    {
        this->physicsData = physicsData;
    }

    bool isValid() const
    {
        bool ok = true;
        ok = ok && !environmentName.empty();
        ok = ok && !libraryName.empty();
        ok = ok && !className.empty();
        ok = ok && !modelFileName.empty();
        ok = ok && !worldFileName.empty();
        ok = ok && actionSpace.isValid();
        ok = ok && observationSpace.isValid();
        ok = ok && physicsData.rtf > 0;
        ok = ok && physicsData.maxStepSize > 0;
        ok = ok && agentRate > 0;
        return ok;
    }
};

#endif // GYMPP_GAZEBO_METADATA
