-- This Source Code Form is subject to the terms of the bCDDL, v. 1.1.
-- If a copy of the bCDDL was not distributed with this
-- file, You can obtain one at http://beamng.com/bCDDL-1.1.txt

-- ========================================================================================================================= --
-- For information on how to implement and distribute your custom UDP protocol, please check https://go.beamng.com/protocols --
-- ========================================================================================================================= --

-- generic outgauge implementation based on LiveForSpeed
local M = {}

local hasShiftLights = false
local function init()
  local shiftLightControllers = controller.getControllersByType("shiftLights")
  hasShiftLights = shiftLightControllers and #shiftLightControllers > 0
end

local function reset() end
local function getAddress()        return settings.getValue("protocols_outgauge_address") end        -- return "127.0.0.1"
local function getPort()           return 4445 end           -- return 4567
local function getMaxUpdateRate()  return settings.getValue("protocols_outgauge_maxUpdateRate") end  -- return 60

local function isPhysicsStepUsed()
  return false -- use graphics step. performance cost is ok. the update rate could reach UP TO min(getMaxUpdateRate(), graphicsFramerate)
  --return true-- use physics step. performance cost is big. the update rate could reach UP TO min(getMaxUpdateRate(), 2000 Hz)
end

local function getStructDefinition()
  -- the original protocol documentation can be found at LFS/docs/InSim.txt
  return [[
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////// IMPORTANT: if you modify this definition, also update the docs at https://go.beamng.com/protocols /////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    char           car[16];         // Car name
    char           gear[4];         // Gears
    float          wheelSpeed;      // M/S
    float          airSpeed;        // M/S
    float          rpm;             // RPM
    float          rpmMax;          // RPM Max
    float          boost;           // BAR
    float          boostMax;        // BAR
    float          engTemp;         // C
    float          oilTemp;         // C
    float          fuel;            // 0 to 1
    float          throttle;        // 0 to 1
    float          brake;           // 0 to 1
    float          clutch;          // 0 to 1
    float          lights;          // lights
    int            parkingbrake;    // parkingbrake
    int            signal_L;        // signal_L
    int            signal_R;        // signal_R
    int            abs;             // abs
    int            engineRunning;   // engineRunning
    int            checkengine;     // checkengine
    int            esc;             // esc
    int            tcs;             // tcs
    int            ev;              // Is EV
  ]]
end

local function fillStruct(o, dtSim)
  local ev = 0
  if v.data.frontMotor or v.data.rearMotor then
	ev = 1
  end
  o.car = v.config.model or ""
  o.gear = tostring(electrics.values.gear) or 0
  o.wheelSpeed = electrics.values.wheelspeed or 0
  o.airSpeed = electrics.values.airspeed or 0
  o.rpm = electrics.values.rpm or 0
  o.rpmMax = electrics.values.maxrpm or 0
  o.boost = electrics.values.boost or 0
  o.boostMax = electrics.values.boostMax or 0
  o.engTemp = electrics.values.watertemp or 0
  o.oilTemp = electrics.values.oiltemp or 0
  o.fuel = electrics.values.fuel or 0
  o.throttle = electrics.values.throttle or 0
  o.brake = electrics.values.brake or 0
  o.clutch = electrics.values.clutch or 0
  o.lights = electrics.values.lights_state or 0
  o.parkingbrake = electrics.values.parkingbrake or 0
  o.signal_L = electrics.values.signal_L or 0
  o.signal_R = electrics.values.signal_R or 0
  o.abs = electrics.values.abs or 0
  o.engineRunning = electrics.values.engineRunning or 0
  o.checkengine = electrics.values.checkengine or 0
  o.esc = electrics.values.esc or 0
  o.tcs = electrics.values.tcs or 0
  o.ev = ev
  -- print("=============")
  -- for key, value in pairs(electrics.values) do
	-- print(key, value)
  -- end 
end

M.init = init
M.reset = reset
M.getAddress = getAddress
M.getPort = getPort
M.getMaxUpdateRate = getMaxUpdateRate
M.getStructDefinition = getStructDefinition
M.fillStruct = fillStruct
M.isPhysicsStepUsed = isPhysicsStepUsed

return M
