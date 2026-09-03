local M = {}

local function onExtensionLoaded()

end

local function onUpdate(dt, dtSim)
    local tod = core_environment.getTimeOfDay()

    be:sendToMailbox("notdbrandTime", tod.time)
end

M.onExtensionLoaded = onExtensionLoaded
M.onVehicleSwitched = onExtensionLoaded
M.onVehicleDestroyed = onExtensionLoaded
M.onVehicleSpawned = onExtensionLoaded
M.onClientPostStartMission = onExtensionLoaded
M.registerVehicle = onExtensionLoaded
M.onUpdate = onUpdate
return M