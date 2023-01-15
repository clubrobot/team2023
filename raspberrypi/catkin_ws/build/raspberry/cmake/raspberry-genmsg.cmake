# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "raspberry: 1 messages, 0 services")

set(MSG_I_FLAGS "-Iraspberry:/home/leproblemededmn/CRobot/team2023/team2023/raspberrypi/catkin_ws/src/raspberry/std_msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(raspberry_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/leproblemededmn/CRobot/team2023/team2023/raspberrypi/catkin_ws/src/raspberry/std_msg/tos_data.msg" NAME_WE)
add_custom_target(_raspberry_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "raspberry" "/home/leproblemededmn/CRobot/team2023/team2023/raspberrypi/catkin_ws/src/raspberry/std_msg/tos_data.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(raspberry
  "/home/leproblemededmn/CRobot/team2023/team2023/raspberrypi/catkin_ws/src/raspberry/std_msg/tos_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/raspberry
)

### Generating Services

### Generating Module File
_generate_module_cpp(raspberry
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/raspberry
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(raspberry_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(raspberry_generate_messages raspberry_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/leproblemededmn/CRobot/team2023/team2023/raspberrypi/catkin_ws/src/raspberry/std_msg/tos_data.msg" NAME_WE)
add_dependencies(raspberry_generate_messages_cpp _raspberry_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(raspberry_gencpp)
add_dependencies(raspberry_gencpp raspberry_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS raspberry_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(raspberry
  "/home/leproblemededmn/CRobot/team2023/team2023/raspberrypi/catkin_ws/src/raspberry/std_msg/tos_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/raspberry
)

### Generating Services

### Generating Module File
_generate_module_eus(raspberry
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/raspberry
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(raspberry_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(raspberry_generate_messages raspberry_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/leproblemededmn/CRobot/team2023/team2023/raspberrypi/catkin_ws/src/raspberry/std_msg/tos_data.msg" NAME_WE)
add_dependencies(raspberry_generate_messages_eus _raspberry_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(raspberry_geneus)
add_dependencies(raspberry_geneus raspberry_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS raspberry_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(raspberry
  "/home/leproblemededmn/CRobot/team2023/team2023/raspberrypi/catkin_ws/src/raspberry/std_msg/tos_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/raspberry
)

### Generating Services

### Generating Module File
_generate_module_lisp(raspberry
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/raspberry
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(raspberry_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(raspberry_generate_messages raspberry_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/leproblemededmn/CRobot/team2023/team2023/raspberrypi/catkin_ws/src/raspberry/std_msg/tos_data.msg" NAME_WE)
add_dependencies(raspberry_generate_messages_lisp _raspberry_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(raspberry_genlisp)
add_dependencies(raspberry_genlisp raspberry_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS raspberry_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(raspberry
  "/home/leproblemededmn/CRobot/team2023/team2023/raspberrypi/catkin_ws/src/raspberry/std_msg/tos_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/raspberry
)

### Generating Services

### Generating Module File
_generate_module_nodejs(raspberry
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/raspberry
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(raspberry_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(raspberry_generate_messages raspberry_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/leproblemededmn/CRobot/team2023/team2023/raspberrypi/catkin_ws/src/raspberry/std_msg/tos_data.msg" NAME_WE)
add_dependencies(raspberry_generate_messages_nodejs _raspberry_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(raspberry_gennodejs)
add_dependencies(raspberry_gennodejs raspberry_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS raspberry_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(raspberry
  "/home/leproblemededmn/CRobot/team2023/team2023/raspberrypi/catkin_ws/src/raspberry/std_msg/tos_data.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/raspberry
)

### Generating Services

### Generating Module File
_generate_module_py(raspberry
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/raspberry
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(raspberry_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(raspberry_generate_messages raspberry_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/leproblemededmn/CRobot/team2023/team2023/raspberrypi/catkin_ws/src/raspberry/std_msg/tos_data.msg" NAME_WE)
add_dependencies(raspberry_generate_messages_py _raspberry_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(raspberry_genpy)
add_dependencies(raspberry_genpy raspberry_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS raspberry_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/raspberry)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/raspberry
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(raspberry_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/raspberry)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/raspberry
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(raspberry_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/raspberry)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/raspberry
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(raspberry_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/raspberry)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/raspberry
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(raspberry_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/raspberry)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/raspberry\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/raspberry
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(raspberry_generate_messages_py std_msgs_generate_messages_py)
endif()
