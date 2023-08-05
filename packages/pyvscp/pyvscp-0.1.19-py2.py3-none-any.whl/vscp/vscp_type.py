# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#  This file is part of VSCP - Very Simple Control Protocol
#  http://www.vscp.org
#
# ******************************************************************************


#
#            !!!!!!!!!!!!!!!!!!!!  W A R N I N G  !!!!!!!!!!!!!!!!!!!!
#                           This file is auto-generated
#                see https://github.com/grodansparadis/vscp-classes
#                        Generated: 2020-06-11 14:08:13.817488
#
 
 
VSCP_TYPE_UNDEFINED                                  = 0

#  CLASS1.PROTOCOL = 0  -  VSCP Protocol Functionality
VSCP_TYPE_PROTOCOL_GENERAL                           = 0 # General event.
VSCP_TYPE_PROTOCOL_SEGCTRL_HEARTBEAT                 = 1 # Segment Controller Heartbeat.
VSCP_TYPE_PROTOCOL_NEW_NODE_ONLINE                   = 2 # New node on line / Probe.
VSCP_TYPE_PROTOCOL_PROBE_ACK                         = 3 # Probe ACK.
VSCP_TYPE_PROTOCOL_RESERVED4                         = 4 # Reserved for future use.
VSCP_TYPE_PROTOCOL_RESERVED5                         = 5 # Reserved for future use.
VSCP_TYPE_PROTOCOL_SET_NICKNAME                      = 6 # Set nickname-ID for node.
VSCP_TYPE_PROTOCOL_NICKNAME_ACCEPTED                 = 7 # Nickname-ID accepted.
VSCP_TYPE_PROTOCOL_DROP_NICKNAME                     = 8 # Drop nickname-ID / Reset Device.
VSCP_TYPE_PROTOCOL_READ_REGISTER                     = 9 # Read register.
VSCP_TYPE_PROTOCOL_RW_RESPONSE                       = 10 # Read/Write response.
VSCP_TYPE_PROTOCOL_WRITE_REGISTER                    = 11 # Write register.
VSCP_TYPE_PROTOCOL_ENTER_BOOT_LOADER                 = 12 # Enter boot loader mode.
VSCP_TYPE_PROTOCOL_ACK_BOOT_LOADER                   = 13 # ACK boot loader mode.
VSCP_TYPE_PROTOCOL_NACK_BOOT_LOADER                  = 14 # NACK boot loader mode.
VSCP_TYPE_PROTOCOL_START_BLOCK                       = 15 # Start block data transfer.
VSCP_TYPE_PROTOCOL_BLOCK_DATA                        = 16 # Block data.
VSCP_TYPE_PROTOCOL_BLOCK_DATA_ACK                    = 17 # ACK data block.
VSCP_TYPE_PROTOCOL_BLOCK_DATA_NACK                   = 18 # NACK data block.
VSCP_TYPE_PROTOCOL_PROGRAM_BLOCK_DATA                = 19 # Program data block.
VSCP_TYPE_PROTOCOL_PROGRAM_BLOCK_DATA_ACK            = 20 # ACK program data block.
VSCP_TYPE_PROTOCOL_PROGRAM_BLOCK_DATA_NACK           = 21 # NACK program data block.
VSCP_TYPE_PROTOCOL_ACTIVATE_NEW_IMAGE                = 22 # Activate new image.
VSCP_TYPE_PROTOCOL_RESET_DEVICE                      = 23 # GUID drop nickname-ID / reset device.
VSCP_TYPE_PROTOCOL_PAGE_READ                         = 24 # Page read.
VSCP_TYPE_PROTOCOL_PAGE_WRITE                        = 25 # Page write.
VSCP_TYPE_PROTOCOL_RW_PAGE_RESPONSE                  = 26 # Read/Write page response.
VSCP_TYPE_PROTOCOL_HIGH_END_SERVER_PROBE             = 27 # High end server/service probe.
VSCP_TYPE_PROTOCOL_HIGH_END_SERVER_RESPONSE          = 28 # High end server/service response.
VSCP_TYPE_PROTOCOL_INCREMENT_REGISTER                = 29 # Increment register.
VSCP_TYPE_PROTOCOL_DECREMENT_REGISTER                = 30 # Decrement register.
VSCP_TYPE_PROTOCOL_WHO_IS_THERE                      = 31 # Who is there?
VSCP_TYPE_PROTOCOL_WHO_IS_THERE_RESPONSE             = 32 # Who is there response.
VSCP_TYPE_PROTOCOL_GET_MATRIX_INFO                   = 33 # Get decision matrix info.
VSCP_TYPE_PROTOCOL_GET_MATRIX_INFO_RESPONSE          = 34 # Decision matrix info response.
VSCP_TYPE_PROTOCOL_GET_EMBEDDED_MDF                  = 35 # Get embedded MDF.
VSCP_TYPE_PROTOCOL_GET_EMBEDDED_MDF_RESPONSE         = 36 # Embedded MDF response.
VSCP_TYPE_PROTOCOL_EXTENDED_PAGE_READ                = 37 # Extended page read register.
VSCP_TYPE_PROTOCOL_EXTENDED_PAGE_WRITE               = 38 # Extended page write register.
VSCP_TYPE_PROTOCOL_EXTENDED_PAGE_RESPONSE            = 39 # Extended page read/write response.
VSCP_TYPE_PROTOCOL_GET_EVENT_INTEREST                = 40 # Get event interest.
VSCP_TYPE_PROTOCOL_GET_EVENT_INTEREST_RESPONSE       = 41 # Get event interest response.
VSCP_TYPE_PROTOCOL_ACTIVATE_NEW_IMAGE_ACK            = 48 # Activate new image ACK.
VSCP_TYPE_PROTOCOL_ACTIVATE_NEW_IMAGE_NACK           = 49 # Activate new image NACK.
VSCP_TYPE_PROTOCOL_START_BLOCK_ACK                   = 50 # Block data transfer ACK.
VSCP_TYPE_PROTOCOL_START_BLOCK_NACK                  = 51 # Block data transfer NACK.

#  CLASS1.ALARM = 1  -  Alarm functionality
VSCP_TYPE_ALARM_GENERAL                              = 0 # General event
VSCP_TYPE_ALARM_WARNING                              = 1 # Warning
VSCP_TYPE_ALARM_ALARM                                = 2 # Alarm occurred
VSCP_TYPE_ALARM_SOUND                                = 3 # Alarm sound on/off
VSCP_TYPE_ALARM_LIGHT                                = 4 # Alarm light on/off
VSCP_TYPE_ALARM_POWER                                = 5 # Power on/off
VSCP_TYPE_ALARM_EMERGENCY_STOP                       = 6 # Emergency Stop
VSCP_TYPE_ALARM_EMERGENCY_PAUSE                      = 7 # Emergency Pause
VSCP_TYPE_ALARM_EMERGENCY_RESET                      = 8 # Emergency Reset
VSCP_TYPE_ALARM_EMERGENCY_RESUME                     = 9 # Emergency Resume
VSCP_TYPE_ALARM_ARM                                  = 10 # Arm
VSCP_TYPE_ALARM_DISARM                               = 11 # Disarm
VSCP_TYPE_ALARM_WATCHDOG                             = 12 # Watchdog

#  CLASS1.SECURITY = 2  -  Security
VSCP_TYPE_SECURITY_GENERAL                           = 0 # General event
VSCP_TYPE_SECURITY_MOTION                            = 1 # Motion Detect
VSCP_TYPE_SECURITY_GLASS_BREAK                       = 2 # Glass break
VSCP_TYPE_SECURITY_BEAM_BREAK                        = 3 # Beam break
VSCP_TYPE_SECURITY_SENSOR_TAMPER                     = 4 # Sensor tamper
VSCP_TYPE_SECURITY_SHOCK_SENSOR                      = 5 # Shock sensor
VSCP_TYPE_SECURITY_SMOKE_SENSOR                      = 6 # Smoke sensor
VSCP_TYPE_SECURITY_HEAT_SENSOR                       = 7 # Heat sensor
VSCP_TYPE_SECURITY_PANIC_SWITCH                      = 8 # Panic switch
VSCP_TYPE_SECURITY_DOOR_OPEN                         = 9 # Door Contact
VSCP_TYPE_SECURITY_WINDOW_OPEN                       = 10 # Window Contact
VSCP_TYPE_SECURITY_CO_SENSOR                         = 11 # CO Sensor
VSCP_TYPE_SECURITY_FROST_DETECTED                    = 12 # Frost detected
VSCP_TYPE_SECURITY_FLAME_DETECTED                    = 13 # Flame detected
VSCP_TYPE_SECURITY_OXYGEN_LOW                        = 14 # Oxygen Low
VSCP_TYPE_SECURITY_WEIGHT_DETECTED                   = 15 # Weight detected.
VSCP_TYPE_SECURITY_WATER_DETECTED                    = 16 # Water detected.
VSCP_TYPE_SECURITY_CONDENSATION_DETECTED             = 17 # Condensation detected.
VSCP_TYPE_SECURITY_SOUND_DETECTED                    = 18 # Noise (sound) detected.
VSCP_TYPE_SECURITY_HARMFUL_SOUND_LEVEL               = 19 # Harmful sound levels detected.
VSCP_TYPE_SECURITY_TAMPER                            = 20 # Tamper detected.
VSCP_TYPE_SECURITY_AUTHENTICATED                     = 21 # Authenticated
VSCP_TYPE_SECURITY_UNAUTHENTICATED                   = 22 # Unauthenticated
VSCP_TYPE_SECURITY_AUTHORIZED                        = 23 # Authorized
VSCP_TYPE_SECURITY_UNAUTHORIZED                      = 24 # Unauthorized
VSCP_TYPE_SECURITY_ID_CHECK                          = 25 # ID check
VSCP_TYPE_SECURITY_PIN_OK                            = 26 # Valid pin
VSCP_TYPE_SECURITY_PIN_FAIL                          = 27 # Invalid pin
VSCP_TYPE_SECURITY_PIN_WARNING                       = 28 # Pin warning
VSCP_TYPE_SECURITY_PIN_ERROR                         = 29 # Pin error
VSCP_TYPE_SECURITY_PASSWORD_OK                       = 30 # Valid password
VSCP_TYPE_SECURITY_PASSWORD_FAIL                     = 31 # Invalid password
VSCP_TYPE_SECURITY_PASSWORD_WARNING                  = 32 # Password warning
VSCP_TYPE_SECURITY_PASSWORD_ERROR                    = 33 # Password error

#  CLASS1.MEASUREMENT = 10  -  Measurement
VSCP_TYPE_MEASUREMENT_GENERAL                        = 0 # General event
VSCP_TYPE_MEASUREMENT_COUNT                          = 1 # Count
VSCP_TYPE_MEASUREMENT_LENGTH                         = 2 # Length/Distance
VSCP_TYPE_MEASUREMENT_MASS                           = 3 # Mass
VSCP_TYPE_MEASUREMENT_TIME                           = 4 # Time
VSCP_TYPE_MEASUREMENT_ELECTRIC_CURRENT               = 5 # Electric Current
VSCP_TYPE_MEASUREMENT_TEMPERATURE                    = 6 # Temperature
VSCP_TYPE_MEASUREMENT_AMOUNT_OF_SUBSTANCE            = 7 # Amount of substance
VSCP_TYPE_MEASUREMENT_INTENSITY_OF_LIGHT             = 8 # Luminous Intensity (Intensity of light)
VSCP_TYPE_MEASUREMENT_FREQUENCY                      = 9 # Frequency
VSCP_TYPE_MEASUREMENT_RADIOACTIVITY                  = 10 # Radioactivity and other random events
VSCP_TYPE_MEASUREMENT_FORCE                          = 11 # Force
VSCP_TYPE_MEASUREMENT_PRESSURE                       = 12 # Pressure
VSCP_TYPE_MEASUREMENT_ENERGY                         = 13 # Energy
VSCP_TYPE_MEASUREMENT_POWER                          = 14 # Power
VSCP_TYPE_MEASUREMENT_ELECTRICAL_CHARGE              = 15 # Electrical Charge
VSCP_TYPE_MEASUREMENT_ELECTRICAL_POTENTIAL           = 16 # Electrical Potential (Voltage)
VSCP_TYPE_MEASUREMENT_ELECTRICAL_CAPACITANCE         = 17 # Electrical Capacitance
VSCP_TYPE_MEASUREMENT_ELECTRICAL_RESISTANCE          = 18 # Electrical Resistance
VSCP_TYPE_MEASUREMENT_ELECTRICAL_CONDUCTANCE         = 19 # Electrical Conductance
VSCP_TYPE_MEASUREMENT_MAGNETIC_FIELD_STRENGTH        = 20 # Magnetic Field Strength
VSCP_TYPE_MEASUREMENT_MAGNETIC_FLUX                  = 21 # Magnetic Flux
VSCP_TYPE_MEASUREMENT_MAGNETIC_FLUX_DENSITY          = 22 # Magnetic Flux Density
VSCP_TYPE_MEASUREMENT_INDUCTANCE                     = 23 # Inductance
VSCP_TYPE_MEASUREMENT_FLUX_OF_LIGHT                  = 24 # Luminous Flux
VSCP_TYPE_MEASUREMENT_ILLUMINANCE                    = 25 # Illuminance
VSCP_TYPE_MEASUREMENT_RADIATION_DOSE_ABSORBED        = 26 # Radiation dose (absorbed)
VSCP_TYPE_MEASUREMENT_CATALYTIC_ACITIVITY            = 27 # Catalytic activity
VSCP_TYPE_MEASUREMENT_VOLUME                         = 28 # Volume
VSCP_TYPE_MEASUREMENT_SOUND_INTENSITY                = 29 # Sound intensity
VSCP_TYPE_MEASUREMENT_ANGLE                          = 30 # Angle
VSCP_TYPE_MEASUREMENT_POSITION                       = 31 # Position WGS 84
VSCP_TYPE_MEASUREMENT_SPEED                          = 32 # Speed
VSCP_TYPE_MEASUREMENT_ACCELERATION                   = 33 # Acceleration
VSCP_TYPE_MEASUREMENT_TENSION                        = 34 # Tension
VSCP_TYPE_MEASUREMENT_HUMIDITY                       = 35 # Damp/moist (Hygrometer reading)
VSCP_TYPE_MEASUREMENT_FLOW                           = 36 # Flow
VSCP_TYPE_MEASUREMENT_THERMAL_RESISTANCE             = 37 # Thermal resistance
VSCP_TYPE_MEASUREMENT_REFRACTIVE_POWER               = 38 # Refractive (optical) power
VSCP_TYPE_MEASUREMENT_DYNAMIC_VISCOSITY              = 39 # Dynamic viscosity
VSCP_TYPE_MEASUREMENT_SOUND_IMPEDANCE                = 40 # Sound impedance
VSCP_TYPE_MEASUREMENT_SOUND_RESISTANCE               = 41 # Sound resistance
VSCP_TYPE_MEASUREMENT_ELECTRIC_ELASTANCE             = 42 # Electric elastance
VSCP_TYPE_MEASUREMENT_LUMINOUS_ENERGY                = 43 # Luminous energy
VSCP_TYPE_MEASUREMENT_LUMINANCE                      = 44 # Luminance
VSCP_TYPE_MEASUREMENT_CHEMICAL_CONCENTRATION_MOLAR   = 45 # Chemical (molar) concentration
VSCP_TYPE_MEASUREMENT_CHEMICAL_CONCENTRATION_MASS    = 46 # Chemical (mass) concentration
VSCP_TYPE_MEASUREMENT_DOSE_EQVIVALENT                = 47 # Reserved
VSCP_TYPE_MEASUREMENT_RESERVED48                     = 48 # Reserved
VSCP_TYPE_MEASUREMENT_DEWPOINT                       = 49 # Dew Point
VSCP_TYPE_MEASUREMENT_RELATIVE_LEVEL                 = 50 # Relative Level
VSCP_TYPE_MEASUREMENT_ALTITUDE                       = 51 # Altitude
VSCP_TYPE_MEASUREMENT_AREA                           = 52 # Area
VSCP_TYPE_MEASUREMENT_RADIANT_INTENSITY              = 53 # Radiant intensity
VSCP_TYPE_MEASUREMENT_RADIANCE                       = 54 # Radiance
VSCP_TYPE_MEASUREMENT_IRRADIANCE                     = 55 # Irradiance, Exitance, Radiosity
VSCP_TYPE_MEASUREMENT_SPECTRAL_RADIANCE              = 56 # Spectral radiance
VSCP_TYPE_MEASUREMENT_SPECTRAL_IRRADIANCE            = 57 # Spectral irradiance
VSCP_TYPE_MEASUREMENT_SOUND_PRESSURE                 = 58 # Sound pressure (acoustic pressure)
VSCP_TYPE_MEASUREMENT_SOUND_DENSITY                  = 59 # Sound energy density
VSCP_TYPE_MEASUREMENT_SOUND_LEVEL                    = 60 # Sound level
VSCP_TYPE_MEASUREMENT_RADIATION_DOSE_EQ              = 61 # Radiation dose (equivalent)
VSCP_TYPE_MEASUREMENT_RADIATION_DOSE_EXPOSURE        = 62 # Radiation dose (exposure)

#  CLASS1.MEASUREMENTX1 = 11  -  Measurement
VSCP_TYPE_MEASUREMENTX1_GENERAL                      = 0 # General event

#  CLASS1.MEASUREMENTX2 = 12  -  Measurement
VSCP_TYPE_MEASUREMENTX2_GENERAL                      = 0 # General event

#  CLASS1.MEASUREMENTX3 = 13  -  Measurement
VSCP_TYPE_MEASUREMENTX3_GENERAL                      = 0 # General event

#  CLASS1.MEASUREMENTX4 = 14  -  Measurement
VSCP_TYPE_MEASUREMENTX4_GENERAL                      = 0 # General event

#  CLASS1.DATA = 15  -  Data
VSCP_TYPE_DATA_GENERAL                               = 0 # General event
VSCP_TYPE_DATA_IO                                    = 1 # I/O value
VSCP_TYPE_DATA_AD                                    = 2 # A/D value
VSCP_TYPE_DATA_DA                                    = 3 # D/A value
VSCP_TYPE_DATA_RELATIVE_STRENGTH                     = 4 # Relative strength
VSCP_TYPE_DATA_SIGNAL_LEVEL                          = 5 # Signal Level
VSCP_TYPE_DATA_SIGNAL_QUALITY                        = 6 # Signal Quality

#  CLASS1.INFORMATION = 20  -  Information
VSCP_TYPE_INFORMATION_GENERAL                        = 0 # General event
VSCP_TYPE_INFORMATION_BUTTON                         = 1 # Button
VSCP_TYPE_INFORMATION_MOUSE                          = 2 # Mouse
VSCP_TYPE_INFORMATION_ON                             = 3 # On
VSCP_TYPE_INFORMATION_OFF                            = 4 # Off
VSCP_TYPE_INFORMATION_ALIVE                          = 5 # Alive
VSCP_TYPE_INFORMATION_TERMINATING                    = 6 # Terminating
VSCP_TYPE_INFORMATION_OPENED                         = 7 # Opened
VSCP_TYPE_INFORMATION_CLOSED                         = 8 # Closed
VSCP_TYPE_INFORMATION_NODE_HEARTBEAT                 = 9 # Node Heartbeat
VSCP_TYPE_INFORMATION_BELOW_LIMIT                    = 10 # Below limit
VSCP_TYPE_INFORMATION_ABOVE_LIMIT                    = 11 # Above limit
VSCP_TYPE_INFORMATION_PULSE                          = 12 # Pulse
VSCP_TYPE_INFORMATION_ERROR                          = 13 # Error
VSCP_TYPE_INFORMATION_RESUMED                        = 14 # Resumed
VSCP_TYPE_INFORMATION_PAUSED                         = 15 # Paused
VSCP_TYPE_INFORMATION_SLEEP                          = 16 # Sleeping
VSCP_TYPE_INFORMATION_GOOD_MORNING                   = 17 # Good morning
VSCP_TYPE_INFORMATION_GOOD_DAY                       = 18 # Good day
VSCP_TYPE_INFORMATION_GOOD_AFTERNOON                 = 19 # Good afternoon
VSCP_TYPE_INFORMATION_GOOD_EVENING                   = 20 # Good evening
VSCP_TYPE_INFORMATION_GOOD_NIGHT                     = 21 # Good night
VSCP_TYPE_INFORMATION_SEE_YOU_SOON                   = 22 # See you soon
VSCP_TYPE_INFORMATION_GOODBYE                        = 23 # Goodbye
VSCP_TYPE_INFORMATION_STOP                           = 24 # Stop
VSCP_TYPE_INFORMATION_START                          = 25 # Start
VSCP_TYPE_INFORMATION_RESET_COMPLETED                = 26 # ResetCompleted
VSCP_TYPE_INFORMATION_INTERRUPTED                    = 27 # Interrupted
VSCP_TYPE_INFORMATION_PREPARING_TO_SLEEP             = 28 # PreparingToSleep
VSCP_TYPE_INFORMATION_WOKEN_UP                       = 29 # WokenUp
VSCP_TYPE_INFORMATION_DUSK                           = 30 # Dusk
VSCP_TYPE_INFORMATION_DAWN                           = 31 # Dawn
VSCP_TYPE_INFORMATION_ACTIVE                         = 32 # Active
VSCP_TYPE_INFORMATION_INACTIVE                       = 33 # Inactive
VSCP_TYPE_INFORMATION_BUSY                           = 34 # Busy
VSCP_TYPE_INFORMATION_IDLE                           = 35 # Idle
VSCP_TYPE_INFORMATION_STREAM_DATA                    = 36 # Stream Data
VSCP_TYPE_INFORMATION_TOKEN_ACTIVITY                 = 37 # Token Activity
VSCP_TYPE_INFORMATION_STREAM_DATA_WITH_ZONE          = 38 # Stream Data with zone
VSCP_TYPE_INFORMATION_CONFIRM                        = 39 # Confirm
VSCP_TYPE_INFORMATION_LEVEL_CHANGED                  = 40 # Level Changed
VSCP_TYPE_INFORMATION_WARNING                        = 41 # Warning
VSCP_TYPE_INFORMATION_STATE                          = 42 # State
VSCP_TYPE_INFORMATION_ACTION_TRIGGER                 = 43 # Action Trigger
VSCP_TYPE_INFORMATION_SUNRISE                        = 44 # Sunrise
VSCP_TYPE_INFORMATION_SUNSET                         = 45 # Sunset
VSCP_TYPE_INFORMATION_START_OF_RECORD                = 46 # Start of record
VSCP_TYPE_INFORMATION_END_OF_RECORD                  = 47 # End of record
VSCP_TYPE_INFORMATION_PRESET_ACTIVE                  = 48 # Pre-set active
VSCP_TYPE_INFORMATION_DETECT                         = 49 # Detect
VSCP_TYPE_INFORMATION_OVERFLOW                       = 50 # Overflow
VSCP_TYPE_INFORMATION_BIG_LEVEL_CHANGED              = 51 # Big level changed
VSCP_TYPE_INFORMATION_SUNRISE_TWILIGHT_START         = 52 # Civil sunrise twilight time
VSCP_TYPE_INFORMATION_SUNSET_TWILIGHT_START          = 53 # Civil sunset twilight time
VSCP_TYPE_INFORMATION_NAUTICAL_SUNRISE_TWILIGHT_START  = 54 # Nautical sunrise twilight time
VSCP_TYPE_INFORMATION_NAUTICAL_SUNSET_TWILIGHT_START  = 55 # Nautical sunset twilight time
VSCP_TYPE_INFORMATION_ASTRONOMICAL_SUNRISE_TWILIGHT_START  = 56 # Astronomical sunrise twilight time
VSCP_TYPE_INFORMATION_ASTRONOMICAL_SUNSET_TWILIGHT_START  = 57 # Astronomical sunset twilight time
VSCP_TYPE_INFORMATION_CALCULATED_NOON                = 58 # Calculated Noon
VSCP_TYPE_INFORMATION_SHUTTER_UP                     = 59 # Shutter up
VSCP_TYPE_INFORMATION_SHUTTER_DOWN                   = 60 # Shutter down
VSCP_TYPE_INFORMATION_SHUTTER_LEFT                   = 61 # Shutter left
VSCP_TYPE_INFORMATION_SHUTTER_RIGHT                  = 62 # Shutter right
VSCP_TYPE_INFORMATION_SHUTTER_END_TOP                = 63 # Shutter reached top end
VSCP_TYPE_INFORMATION_SHUTTER_END_BOTTOM             = 64 # Shutter reached bottom end
VSCP_TYPE_INFORMATION_SHUTTER_END_MIDDLE             = 65 # Shutter reached middle end
VSCP_TYPE_INFORMATION_SHUTTER_END_PRESET             = 66 # Shutter reached preset end
VSCP_TYPE_INFORMATION_SHUTTER_END_LEFT               = 67 # Shutter reached preset left
VSCP_TYPE_INFORMATION_SHUTTER_END_RIGHT              = 68 # Shutter reached preset right
VSCP_TYPE_INFORMATION_LONG_CLICK                     = 69 # Long click
VSCP_TYPE_INFORMATION_SINGLE_CLICK                   = 70 # Single click
VSCP_TYPE_INFORMATION_DOUBLE_CLICK                   = 71 # Double click
VSCP_TYPE_INFORMATION_DATE                           = 72 # Date
VSCP_TYPE_INFORMATION_TIME                           = 73 # Time
VSCP_TYPE_INFORMATION_WEEKDAY                        = 74 # Weekday
VSCP_TYPE_INFORMATION_LOCK                           = 75 # Lock
VSCP_TYPE_INFORMATION_UNLOCK                         = 76 # Unlock
VSCP_TYPE_INFORMATION_DATETIME                       = 77 # DateTime
VSCP_TYPE_INFORMATION_RISING                         = 78 # Rising
VSCP_TYPE_INFORMATION_FALLING                        = 79 # Falling
VSCP_TYPE_INFORMATION_UPDATED                        = 80 # Updated
VSCP_TYPE_INFORMATION_CONNECT                        = 81 # Connect
VSCP_TYPE_INFORMATION_DISCONNECT                     = 82 # Disconnect
VSCP_TYPE_INFORMATION_RECONNECT                      = 83 # Reconnect
VSCP_TYPE_INFORMATION_ENTER                          = 84 # Enter
VSCP_TYPE_INFORMATION_EXIT                           = 85 # Exit

#  CLASS1.CONTROL = 30  -  Control
VSCP_TYPE_CONTROL_GENERAL                            = 0 # General event
VSCP_TYPE_CONTROL_MUTE                               = 1 # Mute on/off
VSCP_TYPE_CONTROL_ALL_LAMPS                          = 2 # (All) Lamp(s) on/off
VSCP_TYPE_CONTROL_OPEN                               = 3 # Open
VSCP_TYPE_CONTROL_CLOSE                              = 4 # Close
VSCP_TYPE_CONTROL_TURNON                             = 5 # TurnOn
VSCP_TYPE_CONTROL_TURNOFF                            = 6 # TurnOff
VSCP_TYPE_CONTROL_START                              = 7 # Start
VSCP_TYPE_CONTROL_STOP                               = 8 # Stop
VSCP_TYPE_CONTROL_RESET                              = 9 # Reset
VSCP_TYPE_CONTROL_INTERRUPT                          = 10 # Interrupt
VSCP_TYPE_CONTROL_SLEEP                              = 11 # Sleep
VSCP_TYPE_CONTROL_WAKEUP                             = 12 # Wakeup
VSCP_TYPE_CONTROL_RESUME                             = 13 # Resume
VSCP_TYPE_CONTROL_PAUSE                              = 14 # Pause
VSCP_TYPE_CONTROL_ACTIVATE                           = 15 # Activate
VSCP_TYPE_CONTROL_DEACTIVATE                         = 16 # Deactivate
VSCP_TYPE_CONTROL_RESERVED17                         = 17 # Reserved for future use
VSCP_TYPE_CONTROL_RESERVED18                         = 18 # Reserved for future use
VSCP_TYPE_CONTROL_RESERVED19                         = 19 # Reserved for future use
VSCP_TYPE_CONTROL_DIM_LAMPS                          = 20 # Dim lamp(s)
VSCP_TYPE_CONTROL_CHANGE_CHANNEL                     = 21 # Change Channel
VSCP_TYPE_CONTROL_CHANGE_LEVEL                       = 22 # Change Level
VSCP_TYPE_CONTROL_RELATIVE_CHANGE_LEVEL              = 23 # Relative Change Level
VSCP_TYPE_CONTROL_MEASUREMENT_REQUEST                = 24 # Measurement Request
VSCP_TYPE_CONTROL_STREAM_DATA                        = 25 # Stream Data
VSCP_TYPE_CONTROL_SYNC                               = 26 # Sync
VSCP_TYPE_CONTROL_ZONED_STREAM_DATA                  = 27 # Zoned Stream Data
VSCP_TYPE_CONTROL_SET_PRESET                         = 28 # Set Pre-set
VSCP_TYPE_CONTROL_TOGGLE_STATE                       = 29 # Toggle state
VSCP_TYPE_CONTROL_TIMED_PULSE_ON                     = 30 # Timed pulse on
VSCP_TYPE_CONTROL_TIMED_PULSE_OFF                    = 31 # Timed pulse off
VSCP_TYPE_CONTROL_SET_COUNTRY_LANGUAGE               = 32 # Set country/language
VSCP_TYPE_CONTROL_BIG_CHANGE_LEVEL                   = 33 # Big Change level
VSCP_TYPE_CONTROL_SHUTTER_UP                         = 34 # Move shutter up
VSCP_TYPE_CONTROL_SHUTTER_DOWN                       = 35 # Move shutter down
VSCP_TYPE_CONTROL_SHUTTER_LEFT                       = 36 # Move shutter left
VSCP_TYPE_CONTROL_SHUTTER_RIGHT                      = 37 # Move shutter right
VSCP_TYPE_CONTROL_SHUTTER_MIDDLE                     = 38 # Move shutter to middle position
VSCP_TYPE_CONTROL_SHUTTER_PRESET                     = 39 # Move shutter to preset position
VSCP_TYPE_CONTROL_ALL_LAMPS_ON                       = 40 # (All) Lamp(s) on
VSCP_TYPE_CONTROL_ALL_LAMPS_OFF                      = 41 # (All) Lamp(s) off
VSCP_TYPE_CONTROL_LOCK                               = 42 # Lock
VSCP_TYPE_CONTROL_UNLOCK                             = 43 # Unlock
VSCP_TYPE_CONTROL_PWM                                = 44 # PWM set
VSCP_TYPE_CONTROL_TOKEN_LOCK                         = 45 # Lock with token
VSCP_TYPE_CONTROL_TOKEN_UNLOCK                       = 46 # Unlock with token
VSCP_TYPE_CONTROL_SET_SECURITY_LEVEL                 = 47 # Set security level
VSCP_TYPE_CONTROL_SET_SECURITY_PIN                   = 48 # Set security pin
VSCP_TYPE_CONTROL_SET_SECURITY_PASSWORD              = 49 # Set security password
VSCP_TYPE_CONTROL_SET_SECURITY_TOKEN                 = 50 # Set security token
VSCP_TYPE_CONTROL_REQUEST_SECURITY_TOKEN             = 51 # Request new security token

#  CLASS1.MULTIMEDIA = 40  -  Multimedia
VSCP_TYPE_MULTIMEDIA_GENERAL                         = 0 # General event
VSCP_TYPE_MULTIMEDIA_PLAYBACK                        = 1 # Playback
VSCP_TYPE_MULTIMEDIA_NAVIGATOR_KEY_ENG               = 2 # NavigatorKey English
VSCP_TYPE_MULTIMEDIA_ADJUST_CONTRAST                 = 3 # Adjust Contrast
VSCP_TYPE_MULTIMEDIA_ADJUST_FOCUS                    = 4 # Adjust Focus
VSCP_TYPE_MULTIMEDIA_ADJUST_TINT                     = 5 # Adjust Tint
VSCP_TYPE_MULTIMEDIA_ADJUST_COLOUR_BALANCE           = 6 # Adjust Color Balance
VSCP_TYPE_MULTIMEDIA_ADJUST_BRIGHTNESS               = 7 # Adjust Brightness
VSCP_TYPE_MULTIMEDIA_ADJUST_HUE                      = 8 # Adjust Hue
VSCP_TYPE_MULTIMEDIA_ADJUST_BASS                     = 9 # Adjust Bass
VSCP_TYPE_MULTIMEDIA_ADJUST_TREBLE                   = 10 # Adjust Treble
VSCP_TYPE_MULTIMEDIA_ADJUST_MASTER_VOLUME            = 11 # Adjust Master Volume
VSCP_TYPE_MULTIMEDIA_ADJUST_FRONT_VOLUME             = 12 # Adjust Front Volume
VSCP_TYPE_MULTIMEDIA_ADJUST_CENTRE_VOLUME            = 13 # Adjust Center Volume
VSCP_TYPE_MULTIMEDIA_ADJUST_REAR_VOLUME              = 14 # Adjust Rear Volume
VSCP_TYPE_MULTIMEDIA_ADJUST_SIDE_VOLUME              = 15 # Adjust Side Volume
VSCP_TYPE_MULTIMEDIA_RESERVED16                      = 16 # Reserved
VSCP_TYPE_MULTIMEDIA_RESERVED17                      = 17 # Reserved
VSCP_TYPE_MULTIMEDIA_RESERVED18                      = 18 # Reserved
VSCP_TYPE_MULTIMEDIA_RESERVED19                      = 19 # Reserved
VSCP_TYPE_MULTIMEDIA_ADJUST_SELECT_DISK              = 20 # Select Disk
VSCP_TYPE_MULTIMEDIA_ADJUST_SELECT_TRACK             = 21 # Select Track
VSCP_TYPE_MULTIMEDIA_ADJUST_SELECT_ALBUM             = 22 # Select Album/Play list
VSCP_TYPE_MULTIMEDIA_ADJUST_SELECT_CHANNEL           = 23 # Select Channel
VSCP_TYPE_MULTIMEDIA_ADJUST_SELECT_PAGE              = 24 # Select Page
VSCP_TYPE_MULTIMEDIA_ADJUST_SELECT_CHAPTER           = 25 # Select Chapter
VSCP_TYPE_MULTIMEDIA_ADJUST_SELECT_SCREEN_FORMAT     = 26 # Select Screen Format
VSCP_TYPE_MULTIMEDIA_ADJUST_SELECT_INPUT_SOURCE      = 27 # Select Input Source
VSCP_TYPE_MULTIMEDIA_ADJUST_SELECT_OUTPUT            = 28 # Select Output
VSCP_TYPE_MULTIMEDIA_RECORD                          = 29 # Record
VSCP_TYPE_MULTIMEDIA_SET_RECORDING_VOLUME            = 30 # Set Recording Volume
VSCP_TYPE_MULTIMEDIA_TIVO_FUNCTION                   = 40 # Tivo Function
VSCP_TYPE_MULTIMEDIA_GET_CURRENT_TITLE               = 50 # Get Current Title
VSCP_TYPE_MULTIMEDIA_SET_POSITION                    = 51 # Set media position in milliseconds
VSCP_TYPE_MULTIMEDIA_GET_MEDIA_INFO                  = 52 # Get media information
VSCP_TYPE_MULTIMEDIA_REMOVE_ITEM                     = 53 # Remove Item from Album
VSCP_TYPE_MULTIMEDIA_REMOVE_ALL_ITEMS                = 54 # Remove all Items from Album
VSCP_TYPE_MULTIMEDIA_SAVE_ALBUM                      = 55 # Save Album/Play list
VSCP_TYPE_MULTIMEDIA_CONTROL                         = 60 # Multimedia Control
VSCP_TYPE_MULTIMEDIA_CONTROL_RESPONSE                = 61 # Multimedia Control response

#  CLASS1.AOL = 50  -  Alert On LAN
VSCP_TYPE_AOL_GENERAL                                = 0 # General event
VSCP_TYPE_AOL_UNPLUGGED_POWER                        = 1 # System unplugged from power source
VSCP_TYPE_AOL_UNPLUGGED_LAN                          = 2 # System unplugged from network
VSCP_TYPE_AOL_CHASSIS_INTRUSION                      = 3 # Chassis intrusion
VSCP_TYPE_AOL_PROCESSOR_REMOVAL                      = 4 # Processor removal
VSCP_TYPE_AOL_ENVIRONMENT_ERROR                      = 5 # System environmental errors
VSCP_TYPE_AOL_HIGH_TEMPERATURE                       = 6 # High temperature
VSCP_TYPE_AOL_FAN_SPEED                              = 7 # Fan speed problem
VSCP_TYPE_AOL_VOLTAGE_FLUCTUATIONS                   = 8 # Voltage fluctuations
VSCP_TYPE_AOL_OS_ERROR                               = 9 # Operating system errors
VSCP_TYPE_AOL_POWER_ON_ERROR                         = 10 # System power-on error
VSCP_TYPE_AOL_SYSTEM_HUNG                            = 11 # System is hung
VSCP_TYPE_AOL_COMPONENT_FAILURE                      = 12 # Component failure
VSCP_TYPE_AOL_REBOOT_UPON_FAILURE                    = 13 # Remote system reboot upon report of a critical failure
VSCP_TYPE_AOL_REPAIR_OPERATING_SYSTEM                = 14 # Repair Operating System
VSCP_TYPE_AOL_UPDATE_BIOS_IMAGE                      = 15 # Update BIOS image
VSCP_TYPE_AOL_UPDATE_DIAGNOSTIC_PROCEDURE            = 16 # Update Perform other diagnostic procedures

#  CLASS1.MEASUREMENT64 = 60  -  Double precision floating point measurement
# 	Event types is the same as  CLASS1.MEASUREMENT = 10  -  Measurement

#  CLASS1.MEASUREMENT64X1 = 61  -  Double precision floating point measurement
# 	Event types is the same as  CLASS1.MEASUREMENTX1 = 11  -  Measurement

#  CLASS1.MEASUREMENT64X2 = 62  -  Double precision floating point measurement
# 	Event types is the same as  CLASS1.MEASUREMENTX2 = 12  -  Measurement

#  CLASS1.MEASUREMENT64X3 = 63  -  Double precision floating point measurement
# 	Event types is the same as  CLASS1.MEASUREMENTX3 = 13  -  Measurement

#  CLASS1.MEASUREMENT64X4 = 64  -  Double precision floating point measurement
# 	Event types is the same as  CLASS1.MEASUREMENTX4 = 14  -  Measurement

#  CLASS1.MEASUREZONE = 65  -  Measurement with zone
# 	Event types is the same as  CLASS1.MEASUREMENT = 10  -  Measurement

#  CLASS1.MEASUREZONEX1 = 66  -  Measurement with zone
# 	Event types is the same as  CLASS1.MEASUREMENTX1 = 11  -  Measurement

#  CLASS1.MEASUREZONEX2 = 67  -  Measurement with zone
# 	Event types is the same as  CLASS1.MEASUREMENTX2 = 12  -  Measurement

#  CLASS1.MEASUREZONEX3 = 68  -  Measurement with zone
# 	Event types is the same as  CLASS1.MEASUREMENTX3 = 13  -  Measurement

#  CLASS1.MEASUREZONEX4 = 69  -  Measurement with zone
# 	Event types is the same as  CLASS1.MEASUREMENTX4 = 14  -  Measurement

#  CLASS1.MEASUREMENT32 = 70  -  Single precision floating point measurement
# 	Event types is the same as  CLASS1.MEASUREMENT = 10  -  Measurement

#  CLASS1.MEASUREMENT32X1 = 71  -  Single precision floating point measurement
# 	Event types is the same as  CLASS1.MEASUREMENTX1 = 11  -  Measurement

#  CLASS1.MEASUREMENT32X2 = 72  -  Single precision floating point measurement
# 	Event types is the same as  CLASS1.MEASUREMENTX2 = 12  -  Measurement

#  CLASS1.MEASUREMENT32X3 = 73  -  Single precision floating point measurement
# 	Event types is the same as  CLASS1.MEASUREMENTX3 = 13  -  Measurement

#  CLASS1.MEASUREMENT32X4 = 74  -  Single precision floating point measurement
# 	Event types is the same as  CLASS1.MEASUREMENTX4 = 14  -  Measurement

#  CLASS1.SETVALUEZONE = 85  -  Set value with zone
# 	Event types is the same as  CLASS1.MEASUREMENT = 10  -  Measurement

#  CLASS1.SETVALUEZONEX1 = 86  -  Set value with zone
# 	Event types is the same as  CLASS1.MEASUREMENTX1 = 11  -  Measurement

#  CLASS1.SETVALUEZONEX2 = 87  -  Set value with zone
# 	Event types is the same as  CLASS1.MEASUREMENTX2 = 12  -  Measurement

#  CLASS1.SETVALUEZONEX3 = 88  -  Set value with zone
# 	Event types is the same as  CLASS1.MEASUREMENTX3 = 13  -  Measurement

#  CLASS1.SETVALUEZONEX4 = 89  -  Set value with zone
# 	Event types is the same as  CLASS1.MEASUREMENTX4 = 14  -  Measurement

#  CLASS1.WEATHER = 90  -  Weather
VSCP_TYPE_WEATHER_GENERAL                            = 0 # General event
VSCP_TYPE_WEATHER_SEASONS_WINTER                     = 1 # Season winter
VSCP_TYPE_WEATHER_SEASONS_SPRING                     = 2 # Season spring
VSCP_TYPE_WEATHER_SEASONS_SUMMER                     = 3 # Season summer
VSCP_TYPE_WEATHER_SEASONS_AUTUMN                     = 4 # Autumn summer
VSCP_TYPE_WEATHER_WIND_NONE                          = 5 # No wind
VSCP_TYPE_WEATHER_WIND_LOW                           = 6 # Low wind
VSCP_TYPE_WEATHER_WIND_MEDIUM                        = 7 # Medium wind
VSCP_TYPE_WEATHER_WIND_HIGH                          = 8 # High wind
VSCP_TYPE_WEATHER_WIND_VERY_HIGH                     = 9 # Very high wind
VSCP_TYPE_WEATHER_AIR_FOGGY                          = 10 # Air foggy
VSCP_TYPE_WEATHER_AIR_FREEZING                       = 11 # Air freezing
VSCP_TYPE_WEATHER_AIR_VERY_COLD                      = 12 # Air Very cold
VSCP_TYPE_WEATHER_AIR_COLD                           = 13 # Air cold
VSCP_TYPE_WEATHER_AIR_NORMAL                         = 14 # Air normal
VSCP_TYPE_WEATHER_AIR_HOT                            = 15 # Air hot
VSCP_TYPE_WEATHER_AIR_VERY_HOT                       = 16 # Air very hot
VSCP_TYPE_WEATHER_AIR_POLLUTION_LOW                  = 17 # Pollution low
VSCP_TYPE_WEATHER_AIR_POLLUTION_MEDIUM               = 18 # Pollution medium
VSCP_TYPE_WEATHER_AIR_POLLUTION_HIGH                 = 19 # Pollution high
VSCP_TYPE_WEATHER_AIR_HUMID                          = 20 # Air humid
VSCP_TYPE_WEATHER_AIR_DRY                            = 21 # Air dry
VSCP_TYPE_WEATHER_SOIL_HUMID                         = 22 # Soil humid
VSCP_TYPE_WEATHER_SOIL_DRY                           = 23 # Soil dry
VSCP_TYPE_WEATHER_RAIN_NONE                          = 24 # Rain none
VSCP_TYPE_WEATHER_RAIN_LIGHT                         = 25 # Rain light
VSCP_TYPE_WEATHER_RAIN_HEAVY                         = 26 # Rain heavy
VSCP_TYPE_WEATHER_RAIN_VERY_HEAVY                    = 27 # Rain very heavy
VSCP_TYPE_WEATHER_SUN_NONE                           = 28 # Sun none
VSCP_TYPE_WEATHER_SUN_LIGHT                          = 29 # Sun light
VSCP_TYPE_WEATHER_SUN_HEAVY                          = 30 # Sun heavy
VSCP_TYPE_WEATHER_SNOW_NONE                          = 31 # Snow none
VSCP_TYPE_WEATHER_SNOW_LIGHT                         = 32 # Snow light
VSCP_TYPE_WEATHER_SNOW_HEAVY                         = 33 # Snow heavy
VSCP_TYPE_WEATHER_DEW_POINT                          = 34 # Dew point
VSCP_TYPE_WEATHER_STORM                              = 35 # Storm
VSCP_TYPE_WEATHER_FLOOD                              = 36 # Flood
VSCP_TYPE_WEATHER_EARTHQUAKE                         = 37 # Earthquake
VSCP_TYPE_WEATHER_NUCLEAR_DISASTER                   = 38 # Nuclear disaster
VSCP_TYPE_WEATHER_FIRE                               = 39 # Fire
VSCP_TYPE_WEATHER_LIGHTNING                          = 40 # Lightning
VSCP_TYPE_WEATHER_UV_RADIATION_LOW                   = 41 # UV Radiation low
VSCP_TYPE_WEATHER_UV_RADIATION_MEDIUM                = 42 # UV Radiation medium
VSCP_TYPE_WEATHER_UV_RADIATION_NORMAL                = 43 # UV Radiation normal
VSCP_TYPE_WEATHER_UV_RADIATION_HIGH                  = 44 # UV Radiation high
VSCP_TYPE_WEATHER_UV_RADIATION_VERY_HIGH             = 45 # UV Radiation very high
VSCP_TYPE_WEATHER_WARNING_LEVEL1                     = 46 # Warning level 1
VSCP_TYPE_WEATHER_WARNING_LEVEL2                     = 47 # Warning level 2
VSCP_TYPE_WEATHER_WARNING_LEVEL3                     = 48 # Warning level 3
VSCP_TYPE_WEATHER_WARNING_LEVEL4                     = 49 # Warning level 4
VSCP_TYPE_WEATHER_WARNING_LEVEL5                     = 50 # Warning level 5
VSCP_TYPE_WEATHER_ARMAGEDON                          = 51 # Armageddon
VSCP_TYPE_WEATHER_UV_INDEX                           = 52 # UV Index

#  CLASS1.WEATHER_FORECAST = 95  -  Weather forecast
# 	Event types is the same as  CLASS1.WEATHER = 90  -  Weather

#  CLASS1.PHONE = 100  -  Phone
VSCP_TYPE_PHONE_GENERAL                              = 0 # General event
VSCP_TYPE_PHONE_INCOMING_CALL                        = 1 # Incoming call
VSCP_TYPE_PHONE_OUTGOING_CALL                        = 2 # Outgoing call
VSCP_TYPE_PHONE_RING                                 = 3 # Ring
VSCP_TYPE_PHONE_ANSWER                               = 4 # Answer
VSCP_TYPE_PHONE_HANGUP                               = 5 # Hangup
VSCP_TYPE_PHONE_GIVEUP                               = 6 # Giveup
VSCP_TYPE_PHONE_TRANSFER                             = 7 # Transfer
VSCP_TYPE_PHONE_DATABASE_INFO                        = 8 # Database Info

#  CLASS1.DISPLAY = 102  -  Display
VSCP_TYPE_DISPLAY_GENERAL                            = 0 # General event
VSCP_TYPE_DISPLAY_CLEAR_DISPLAY                      = 1 # Clear Display
VSCP_TYPE_DISPLAY_POSITION_CURSOR                    = 2 # Position cursor
VSCP_TYPE_DISPLAY_WRITE_DISPLAY                      = 3 # Write Display
VSCP_TYPE_DISPLAY_WRITE_DISPLAY_BUFFER               = 4 # Write Display buffer
VSCP_TYPE_DISPLAY_SHOW_DISPLAY_BUFFER                = 5 # Show Display Buffer
VSCP_TYPE_DISPLAY_SET_DISPLAY_BUFFER_PARAM           = 6 # Set Display Buffer Parameter
VSCP_TYPE_DISPLAY_SHOW_TEXT                          = 32 # Show Text
VSCP_TYPE_DISPLAY_SHOW_LED                           = 48 # Set LED
VSCP_TYPE_DISPLAY_SHOW_LED_COLOR                     = 49 # Set RGB Color

#  CLASS1.IR = 110  -  IR Remote I/f
VSCP_TYPE_REMOTE_GENERAL                             = 0 # General event
VSCP_TYPE_REMOTE_RC5                                 = 1 # RC5 Send/Receive
VSCP_TYPE_REMOTE_SONY12                              = 3 # SONY 12-bit Send/Receive
VSCP_TYPE_REMOTE_LIRC                                = 32 # LIRC (Linux Infrared Remote Control)
VSCP_TYPE_REMOTE_VSCP                                = 48 # VSCP Abstract Remote Format
VSCP_TYPE_REMOTE_MAPITO                              = 49 # MAPito Remote Format

#  CLASS1.GNSS = 206  -  Position (GNSS)
VSCP_TYPE_GNSS_GENERAL                               = 0 # General event
VSCP_TYPE_GNSS_POSITION                              = 1 # Position
VSCP_TYPE_GNSS_SATELLITES                            = 2 # Satellites

#  CLASS1.WIRELESS = 212  -  Wireless
VSCP_TYPE_WIRELESS_GENERAL                           = 0 # General event
VSCP_TYPE_WIRELESS_GSM_CELL                          = 1 # GSM Cell

#  CLASS1.DIAGNOSTIC = 506  -  Diagnostic
VSCP_TYPE_DIAGNOSTIC_GENERAL                         = 0 # General event
VSCP_TYPE_DIAGNOSTIC_OVERVOLTAGE                     = 1 # Overvoltage
VSCP_TYPE_DIAGNOSTIC_UNDERVOLTAGE                    = 2 # Undervoltage
VSCP_TYPE_DIAGNOSTIC_VBUS_LOW                        = 3 # USB VBUS low
VSCP_TYPE_DIAGNOSTIC_BATTERY_LOW                     = 4 # Battery voltage low
VSCP_TYPE_DIAGNOSTIC_BATTERY_FULL                    = 5 # Battery full voltage
VSCP_TYPE_DIAGNOSTIC_BATTERY_ERROR                   = 6 # Battery error
VSCP_TYPE_DIAGNOSTIC_BATTERY_OK                      = 7 # Battery OK
VSCP_TYPE_DIAGNOSTIC_OVERCURRENT                     = 8 # Over current
VSCP_TYPE_DIAGNOSTIC_CIRCUIT_ERROR                   = 9 # Circuit error
VSCP_TYPE_DIAGNOSTIC_SHORT_CIRCUIT                   = 10 # Short circuit
VSCP_TYPE_DIAGNOSTIC_OPEN_CIRCUIT                    = 11 # Open Circuit
VSCP_TYPE_DIAGNOSTIC_MOIST                           = 12 # Moist
VSCP_TYPE_DIAGNOSTIC_WIRE_FAIL                       = 13 # Wire failure
VSCP_TYPE_DIAGNOSTIC_WIRELESS_FAIL                   = 14 # Wireless faliure
VSCP_TYPE_DIAGNOSTIC_IR_FAIL                         = 15 # IR failure
VSCP_TYPE_DIAGNOSTIC_1WIRE_FAIL                      = 16 # 1-wire failure
VSCP_TYPE_DIAGNOSTIC_RS222_FAIL                      = 17 # RS-222 failure
VSCP_TYPE_DIAGNOSTIC_RS232_FAIL                      = 18 # RS-232 failure
VSCP_TYPE_DIAGNOSTIC_RS423_FAIL                      = 19 # RS-423 failure
VSCP_TYPE_DIAGNOSTIC_RS485_FAIL                      = 20 # RS-485 failure
VSCP_TYPE_DIAGNOSTIC_CAN_FAIL                        = 21 # CAN failure
VSCP_TYPE_DIAGNOSTIC_LAN_FAIL                        = 22 # LAN failure
VSCP_TYPE_DIAGNOSTIC_USB_FAIL                        = 23 # USB failure
VSCP_TYPE_DIAGNOSTIC_WIFI_FAIL                       = 24 # Wifi failure
VSCP_TYPE_DIAGNOSTIC_NFC_RFID_FAIL                   = 25 # NFC/RFID failure
VSCP_TYPE_DIAGNOSTIC_LOW_SIGNAL                      = 26 # Low signal
VSCP_TYPE_DIAGNOSTIC_HIGH_SIGNAL                     = 27 # High signal
VSCP_TYPE_DIAGNOSTIC_ADC_FAIL                        = 28 # ADC failure
VSCP_TYPE_DIAGNOSTIC_ALU_FAIL                        = 29 # ALU failure
VSCP_TYPE_DIAGNOSTIC_ASSERT                          = 30 # Assert
VSCP_TYPE_DIAGNOSTIC_DAC_FAIL                        = 31 # DAC failure
VSCP_TYPE_DIAGNOSTIC_DMA_FAIL                        = 32 # DMA failure
VSCP_TYPE_DIAGNOSTIC_ETH_FAIL                        = 33 # Ethernet failure
VSCP_TYPE_DIAGNOSTIC_EXCEPTION                       = 34 # Exception
VSCP_TYPE_DIAGNOSTIC_FPU_FAIL                        = 35 # FPU failure
VSCP_TYPE_DIAGNOSTIC_GPIO_FAIL                       = 36 # GPIO failure
VSCP_TYPE_DIAGNOSTIC_I2C_FAIL                        = 37 # I2C failure
VSCP_TYPE_DIAGNOSTIC_I2S_FAIL                        = 38 # I2S failure
VSCP_TYPE_DIAGNOSTIC_INVALID_CONFIG                  = 39 # Invalid configuration
VSCP_TYPE_DIAGNOSTIC_MMU_FAIL                        = 40 # MMU failure
VSCP_TYPE_DIAGNOSTIC_NMI                             = 41 # NMI failure
VSCP_TYPE_DIAGNOSTIC_OVERHEAT                        = 42 # Overheat
VSCP_TYPE_DIAGNOSTIC_PLL_FAIL                        = 43 # PLL fail
VSCP_TYPE_DIAGNOSTIC_POR_FAIL                        = 44 # POR failure
VSCP_TYPE_DIAGNOSTIC_PWM_FAIL                        = 45 # PWM failure
VSCP_TYPE_DIAGNOSTIC_RAM_FAIL                        = 46 # RAM failure
VSCP_TYPE_DIAGNOSTIC_ROM_FAIL                        = 47 # ROM failure
VSCP_TYPE_DIAGNOSTIC_SPI_FAIL                        = 48 # SPI failure
VSCP_TYPE_DIAGNOSTIC_STACK_FAIL                      = 49 # Stack failure
VSCP_TYPE_DIAGNOSTIC_LIN_FAIL                        = 50 # LIN bus failure
VSCP_TYPE_DIAGNOSTIC_UART_FAIL                       = 51 # UART failure
VSCP_TYPE_DIAGNOSTIC_UNHANDLED_INT                   = 52 # Unhandled interrupt
VSCP_TYPE_DIAGNOSTIC_MEMORY_FAIL                     = 53 # Memory failure
VSCP_TYPE_DIAGNOSTIC_VARIABLE_RANGE                  = 54 # Variable range failure
VSCP_TYPE_DIAGNOSTIC_WDT                             = 55 # WDT failure
VSCP_TYPE_DIAGNOSTIC_EEPROM_FAIL                     = 56 # EEPROM failure
VSCP_TYPE_DIAGNOSTIC_ENCRYPTION_FAIL                 = 57 # Encryption failure
VSCP_TYPE_DIAGNOSTIC_BAD_USER_INPUT                  = 58 # Bad user input failure
VSCP_TYPE_DIAGNOSTIC_DECRYPTION_FAIL                 = 59 # Decryption failure
VSCP_TYPE_DIAGNOSTIC_NOISE                           = 60 # Noise
VSCP_TYPE_DIAGNOSTIC_BOOTLOADER_FAIL                 = 61 # Boot loader failure
VSCP_TYPE_DIAGNOSTIC_PROGRAMFLOW_FAIL                = 62 # Program flow failure
VSCP_TYPE_DIAGNOSTIC_RTC_FAIL                        = 63 # RTC faiure
VSCP_TYPE_DIAGNOSTIC_SYSTEM_TEST_FAIL                = 64 # System test failure
VSCP_TYPE_DIAGNOSTIC_SENSOR_FAIL                     = 65 # Sensor failure
VSCP_TYPE_DIAGNOSTIC_SAFESTATE                       = 66 # Safe state entered
VSCP_TYPE_DIAGNOSTIC_SIGNAL_IMPLAUSIBLE              = 67 # Signal implausible
VSCP_TYPE_DIAGNOSTIC_STORAGE_FAIL                    = 68 # Storage fail
VSCP_TYPE_DIAGNOSTIC_SELFTEST_FAIL                   = 69 # Self test OK
VSCP_TYPE_DIAGNOSTIC_ESD_EMC_EMI                     = 70 # ESD/EMC/EMI failure
VSCP_TYPE_DIAGNOSTIC_TIMEOUT                         = 71 # Timeout
VSCP_TYPE_DIAGNOSTIC_LCD_FAIL                        = 72 # LCD failure
VSCP_TYPE_DIAGNOSTIC_TOUCHPANEL_FAIL                 = 73 # Touch panel failure
VSCP_TYPE_DIAGNOSTIC_NOLOAD                          = 74 # No load
VSCP_TYPE_DIAGNOSTIC_COOLING_FAIL                    = 75 # Cooling failure
VSCP_TYPE_DIAGNOSTIC_HEATING_FAIL                    = 76 # Heating failure
VSCP_TYPE_DIAGNOSTIC_TX_FAIL                         = 77 # Transmission failure
VSCP_TYPE_DIAGNOSTIC_RX_FAIL                         = 78 # Receiption failure
VSCP_TYPE_DIAGNOSTIC_EXT_IC_FAIL                     = 79 # External IC failure

#  CLASS1.ERROR = 508  -  Error
VSCP_TYPE_ERROR_SUCCESS                              = 0 # Success
VSCP_TYPE_ERROR_ERROR                                = 1 # Error
VSCP_TYPE_ERROR_CHANNEL                              = 7 # Channel error
VSCP_TYPE_ERROR_FIFO_EMPTY                           = 8 # Fifo empty error
VSCP_TYPE_ERROR_FIFO_FULL                            = 9 # Fifo full error
VSCP_TYPE_ERROR_FIFO_SIZE                            = 10 # Fifo size error
VSCP_TYPE_ERROR_FIFO_WAIT                            = 11 # Fifo wait error
VSCP_TYPE_ERROR_GENERIC                              = 12 # Generic error
VSCP_TYPE_ERROR_HARDWARE                             = 13 # Hardware error
VSCP_TYPE_ERROR_INIT_FAIL                            = 14 # initialization error
VSCP_TYPE_ERROR_INIT_MISSING                         = 15 # Missing initialization error
VSCP_TYPE_ERROR_INIT_READY                           = 16 # Initialization ready
VSCP_TYPE_ERROR_NOT_SUPPORTED                        = 17 # Not supported
VSCP_TYPE_ERROR_OVERRUN                              = 18 # Overrun error
VSCP_TYPE_ERROR_RCV_EMPTY                            = 19 # Receiver empty error
VSCP_TYPE_ERROR_REGISTER                             = 20 # Register error
VSCP_TYPE_ERROR_TRM_FULL                             = 21 # Transmitter full error
VSCP_TYPE_ERROR_LIBRARY                              = 28 # Library error
VSCP_TYPE_ERROR_PROCADDRESS                          = 29 # Procedural address error
VSCP_TYPE_ERROR_ONLY_ONE_INSTANCE                    = 30 # Only one instance error
VSCP_TYPE_ERROR_SUB_DRIVER                           = 31 # Sub driver error
VSCP_TYPE_ERROR_TIMEOUT                              = 32 # Timeout error
VSCP_TYPE_ERROR_NOT_OPEN                             = 33 # Not open error
VSCP_TYPE_ERROR_PARAMETER                            = 34 # Parameter error
VSCP_TYPE_ERROR_MEMORY                               = 35 # Memory error
VSCP_TYPE_ERROR_INTERNAL                             = 36 # Internal error
VSCP_TYPE_ERROR_COMMUNICATION                        = 37 # Communication error
VSCP_TYPE_ERROR_USER                                 = 38 # User error
VSCP_TYPE_ERROR_PASSWORD                             = 39 # Password error
VSCP_TYPE_ERROR_CONNECTION                           = 40 # Connection error
VSCP_TYPE_ERROR_INVALID_HANDLE                       = 41 # Invalid handle error
VSCP_TYPE_ERROR_OPERATION_FAILED                     = 42 # Operation failed error
VSCP_TYPE_ERROR_BUFFER_SMALL                         = 43 # Supplied buffer is to small to fit content
VSCP_TYPE_ERROR_ITEM_UNKNOWN                         = 44 # Requested item is unknown
VSCP_TYPE_ERROR_NAME_USED                            = 45 # Name is already in use
VSCP_TYPE_ERROR_DATA_WRITE                           = 46 # Error when writing data
VSCP_TYPE_ERROR_ABORTED                              = 47 # Operation stopped or aborted
VSCP_TYPE_ERROR_INVALID_POINTER                      = 48 # Pointer with invalid value

#  CLASS1.LOG = 509  -  Logging
VSCP_TYPE_LOG_GENERAL                                = 0 # General event
VSCP_TYPE_LOG_MESSAGE                                = 1 # Log event
VSCP_TYPE_LOG_START                                  = 2 # Log Start
VSCP_TYPE_LOG_STOP                                   = 3 # Log Stop
VSCP_TYPE_LOG_LEVEL                                  = 4 # Log Level

#  CLASS1.LABORATORY = 510  -  Laboratory use
VSCP_TYPE_LABORATORY_GENERAL                         = 0 # General event

#  CLASS1.LOCAL = 511  -  Local use
VSCP_TYPE_LOCAL_GENERAL                              = 0 # General event

#  CLASS2.LEVEL1.PROTOCOL = 512  -  Class2 Level I Protocol
# 	Event types is the same as  CLASS1.PROTOCOL = 0  -  VSCP Protocol Functionality

#  CLASS2.LEVEL1.ALARM = 513  -  Class2 Level I Alarm
# 	Event types is the same as  CLASS1.ALARM = 1  -  Alarm functionality

#  CLASS2.LEVEL1.SECURITY = 514  -  Class2 Level I Security
# 	Event types is the same as  CLASS1.SECURITY = 2  -  Security

#  CLASS2.LEVEL1.MEASUREMENT = 522  -  Class2 Level I Measurements
# 	Event types is the same as  CLASS1.MEASUREMENT = 10  -  Measurement

#  CLASS2.LEVEL1.MEASUREMENTX1 = 523  -  Class2 Level I Measurements
# 	Event types is the same as  CLASS1.MEASUREMENTX1 = 11  -  Measurement

#  CLASS2.LEVEL1.MEASUREMENTX2 = 524  -  Class2 Level I Measurements
# 	Event types is the same as  CLASS1.MEASUREMENTX2 = 12  -  Measurement

#  CLASS2.LEVEL1.MEASUREMENTX3 = 525  -  Class2 Level I Measurements
# 	Event types is the same as  CLASS1.MEASUREMENTX3 = 13  -  Measurement

#  CLASS2.LEVEL1.MEASUREMENTX4 = 526  -  Class2 Level I Measurements
# 	Event types is the same as  CLASS1.MEASUREMENTX4 = 14  -  Measurement

#  CLASS2.LEVEL1.DATA = 527  -  Class2 Level I Data
# 	Event types is the same as  CLASS1.DATA = 15  -  Data

#  CLASS2.LEVEL1.INFORMATION1 = 532  -  Class2 Level I Information
# 	Event types is the same as  CLASS1.INFORMATION = 20  -  Information

#  CLASS2.LEVEL1.CONTROL = 542  -  Class2 Level I Control
# 	Event types is the same as  CLASS1.CONTROL = 30  -  Control

#  CLASS2.LEVEL1.MULTIMEDIA = 552  -  Class2 Level I Multimedia
# 	Event types is the same as  CLASS1.MULTIMEDIA = 40  -  Multimedia

#  CLASS2.LEVEL1.AOL = 562  -  Class2 Level I AOL
# 	Event types is the same as  CLASS1.AOL = 50  -  Alert On LAN

#  CLASS2.LEVEL1.MEASUREMENT64 = 572  -  Class2 Level I Measurement64
# 	Event types is the same as  CLASS1.MEASUREMENT = 10  -  Measurement

#  CLASS2.LEVEL1.MEASUREMENT64X1 = 573  -  Class2 Level I Measurement64
# 	Event types is the same as  CLASS1.MEASUREMENTX1 = 11  -  Measurement

#  CLASS2.LEVEL1.MEASUREMENT64X2 = 574  -  Class2 Level I Measurement64
# 	Event types is the same as  CLASS1.MEASUREMENTX2 = 12  -  Measurement

#  CLASS2.LEVEL1.MEASUREMENT64X3 = 575  -  Class2 Level I Measurement64
# 	Event types is the same as  CLASS1.MEASUREMENTX3 = 13  -  Measurement

#  CLASS2.LEVEL1.MEASUREMENT64X4 = 576  -  Class2 Level I Measurement64
# 	Event types is the same as  CLASS1.MEASUREMENTX4 = 14  -  Measurement

#  CLASS2.LEVEL1.MEASUREZONE = 577  -  Class2 Level I Measurementzone
# 	Event types is the same as  CLASS1.MEASUREMENT = 10  -  Measurement

#  CLASS2.LEVEL1.MEASUREZONEX1 = 578  -  Class2 Level I Measurementzone
# 	Event types is the same as  CLASS1.MEASUREMENTX1 = 11  -  Measurement

#  CLASS2.LEVEL1.MEASUREZONEX2 = 579  -  Class2 Level I Measurementzone
# 	Event types is the same as  CLASS1.MEASUREMENTX2 = 12  -  Measurement

#  CLASS2.LEVEL1.MEASUREZONEX3 = 580  -  Class2 Level I Measurementzone
# 	Event types is the same as  CLASS1.MEASUREMENTX3 = 13  -  Measurement

#  CLASS2.LEVEL1.MEASUREZONEX4 = 581  -  Class2 Level I Measurementzone
# 	Event types is the same as  CLASS1.MEASUREMENTX4 = 14  -  Measurement

#  CLASS2.LEVEL1.MEASUREMENT32 = 582  -  Class2 Level I Measuremet32
# 	Event types is the same as  CLASS1.MEASUREMENT = 10  -  Measurement

#  CLASS2.LEVEL1.MEASUREMENT32X1 = 583  -  Class2 Level I Measuremet32
# 	Event types is the same as  CLASS1.MEASUREMENTX1 = 11  -  Measurement

#  CLASS2.LEVEL1.MEASUREMENT32X2 = 584  -  Class2 Level I Measuremet32
# 	Event types is the same as  CLASS1.MEASUREMENTX2 = 12  -  Measurement

#  CLASS2.LEVEL1.MEASUREMENT32X3 = 585  -  Class2 Level I Measuremet32
# 	Event types is the same as  CLASS1.MEASUREMENTX3 = 13  -  Measurement

#  CLASS2.LEVEL1.MEASUREMENT32X4 = 586  -  Class2 Level I Measuremet32
# 	Event types is the same as  CLASS1.MEASUREMENTX4 = 14  -  Measurement

#  CLASS2.LEVEL1.SETVALUEZONE = 597  -  Class2 Level I SetValueZone
# 	Event types is the same as  CLASS1.MEASUREMENT = 10  -  Measurement

#  CLASS2.LEVEL1.SETVALUEZONEX1 = 598  -  Class2 Level I SetValueZone
# 	Event types is the same as  CLASS1.MEASUREMENTX1 = 11  -  Measurement

#  CLASS2.LEVEL1.SETVALUEZONEX2 = 599  -  Class2 Level I SetValueZone
# 	Event types is the same as  CLASS1.MEASUREMENTX2 = 12  -  Measurement

#  CLASS2.LEVEL1.SETVALUEZONEX3 = 600  -  Class2 Level I SetValueZone
# 	Event types is the same as  CLASS1.MEASUREMENTX3 = 13  -  Measurement

#  CLASS2.LEVEL1.SETVALUEZONEX4 = 601  -  Class2 Level I SetValueZone
# 	Event types is the same as  CLASS1.MEASUREMENTX4 = 14  -  Measurement

#  CLASS2.LEVEL1.WEATHER = 602  -  Class2 Level I Weather
# 	Event types is the same as  CLASS1.WEATHER = 90  -  Weather

#  CLASS2.LEVEL1.WEATHERFORECAST = 607  -  Class2 Level I Weather Forecast
# 	Event types is the same as  CLASS1.WEATHER = 90  -  Weather

#  CLASS2.LEVEL1.PHONE = 612  -  Class2 Level I Phone
# 	Event types is the same as  CLASS1.PHONE = 100  -  Phone

#  CLASS2.LEVEL1.DISPLAY = 614  -  Class2 Level I Display
# 	Event types is the same as  CLASS1.DISPLAY = 102  -  Display

#  CLASS2.LEVEL1.IR = 622  -  Class2 Level I IR
# 	Event types is the same as  CLASS1.IR = 110  -  IR Remote I/f

#  CLASS2.LEVEL1.GNSS = 718  -  Class2 Level I GNSS
# 	Event types is the same as  CLASS1.GNSS = 206  -  Position (GNSS)

#  CLASS2.LEVEL1.WIRELESS = 724  -  Class2 Level I Wireless
# 	Event types is the same as  CLASS1.WIRELESS = 212  -  Wireless

#  CLASS2.LEVEL1.DIAGNOSTIC = 1018  -  Class2 Level I Diagnostic
# 	Event types is the same as  CLASS1.DIAGNOSTIC = 506  -  Diagnostic

#  CLASS2.LEVEL1.ERROR = 1020  -  Class2 Level I Error
# 	Event types is the same as  CLASS1.ERROR = 508  -  Error

#  CLASS2.LEVEL1.LOG = 1021  -  Class2 Level I Log
# 	Event types is the same as  CLASS1.LOG = 509  -  Logging

#  CLASS2.LEVEL1.LABORATORY = 1022  -  Class2 Level I Laboratory
# 	Event types is the same as  CLASS1.LABORATORY = 510  -  Laboratory use

#  CLASS2.LEVEL1.LOCAL = 1023  -  Class2 Level I Local
# 	Event types is the same as  CLASS1.LOCAL = 511  -  Local use

#  CLASS2.PROTOCOL = 1024  -  Level II Protocol Functionality
VSCP2_TYPE_PROTOCOL_GENERAL                          = 0 # General event
VSCP2_TYPE_PROTOCOL_READ_REGISTER                    = 1 # Read Register
VSCP2_TYPE_PROTOCOL_WRITE_REGISTER                   = 2 # Write Register
VSCP2_TYPE_PROTOCOL_READ_WRITE_RESPONSE              = 3 # Read Write Response
VSCP2_TYPE_PROTOCOL_HIGH_END_SERVER_CAPS             = 20 # High end server/service capabilities
VSCP2_TYPE_PROTOCOL_WHO_IS_THERE_RESPONSE            = 32 # Level II who is there response

#  CLASS2.CONTROL = 1025  -  Level II Control
VSCP2_TYPE_CONTROL_GENERAL                           = 0 # General event

#  CLASS2.INFORMATION = 1026  -  Level II Information
VSCP2_TYPE_INFORMATION_GENERAL                       = 0 # General event
VSCP2_TYPE_INFORMATION_TOKEN_ACTIVITY                = 1 # Token Activity
VSCP2_TYPE_INFORMATION_HEART_BEAT                    = 2 # Level II Node Heartbeat
VSCP2_TYPE_INFORMATION_PROXY_HEART_BEAT              = 3 # Level II Proxy Node Heartbeat
VSCP2_TYPE_INFORMATION_CHANNEL_ANNOUNCE              = 4 # Level II Multicast channel announce

#  CLASS2.TEXT2SPEECH = 1027  -  Text to speech
VSCP2_TYPE_TEXT2SPEECH_GENERAL                       = 0 # General event
VSCP2_TYPE_TEXT2SPEECH_TALK                          = 1 # Talk

#  CLASS2.HLO = 1028  -  High Level Object
VSCP2_TYPE_HLO_GENERAL                               = 0 # General event
VSCP2_TYPE_HLO_COMMAND                               = 1 # HLO Command
VSCP2_TYPE_HLO_RESPONSE                              = 2 # HLO Response

#  CLASS2.CUSTOM = 1029  -  Level II Custom
VSCP2_TYPE_CUSTOM_GENERAL                            = 0 # General event

#  CLASS2.DISPLAY = 1030  -  Level II Display
VSCP2_TYPE_DISPLAY_GENERAL                           = 0 # General event

#  CLASS2.MEASUREMENT_STR = 1040  -  Measurement string
# 	Event types is the same as  CLASS1.MEASUREMENT = 10  -  Measurement

#  CLASS2.MEASUREMENT_FLOAT = 1060  -  Measurement float
# 	Event types is the same as  CLASS1.MEASUREMENT = 10  -  Measurement

#  CLASS2.VSCPD = 65535  -  VSCP Daemon internal events
VSCP2_TYPE_VSCPD_GENERAL                             = 0 # General event
VSCP2_TYPE_VSCPD_LOOP                                = 1 # Loop
VSCP2_TYPE_VSCPD_PAUSE                               = 3 # Pause
VSCP2_TYPE_VSCPD_ACTIVATE                            = 4 # Activate
VSCP2_TYPE_VSCPD_STARTING_UP                         = 5 # Starting up
VSCP2_TYPE_VSCPD_SHUTTING_DOWN                       = 6 # Shutting down
VSCP2_TYPE_VSCPD_DRV3_START                          = 7 # Start
VSCP2_TYPE_VSCPD_DRV3_STOP                           = 8 # Stop
VSCP2_TYPE_VSCPD_DRV3_PAUSE                          = 9 # Pause
VSCP2_TYPE_VSCPD_DRV3_RESUME                         = 10 # Resume
VSCP2_TYPE_VSCPD_DRV3_RESTART                        = 11 # Restart
VSCP2_TYPE_VSCPD_DRV3_CONFIG                         = 12 # Config
 
 
