; Auto-generated. Do not edit!


(cl:in-package raspberry-msg)


;//! \htmlinclude tos_data.msg.html

(cl:defclass <tos_data> (roslisp-msg-protocol:ros-message)
  ((angle
    :reader angle
    :initarg :angle
    :type cl:float
    :initform 0.0)
   (modalite
    :reader modalite
    :initarg :modalite
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass tos_data (<tos_data>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <tos_data>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'tos_data)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name raspberry-msg:<tos_data> is deprecated: use raspberry-msg:tos_data instead.")))

(cl:ensure-generic-function 'angle-val :lambda-list '(m))
(cl:defmethod angle-val ((m <tos_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader raspberry-msg:angle-val is deprecated.  Use raspberry-msg:angle instead.")
  (angle m))

(cl:ensure-generic-function 'modalite-val :lambda-list '(m))
(cl:defmethod modalite-val ((m <tos_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader raspberry-msg:modalite-val is deprecated.  Use raspberry-msg:modalite instead.")
  (modalite m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <tos_data>) ostream)
  "Serializes a message object of type '<tos_data>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'angle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'modalite) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <tos_data>) istream)
  "Deserializes a message object of type '<tos_data>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angle) (roslisp-utils:decode-single-float-bits bits)))
    (cl:setf (cl:slot-value msg 'modalite) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<tos_data>)))
  "Returns string type for a message object of type '<tos_data>"
  "raspberry/tos_data")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'tos_data)))
  "Returns string type for a message object of type 'tos_data"
  "raspberry/tos_data")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<tos_data>)))
  "Returns md5sum for a message object of type '<tos_data>"
  "b2965ddc92e8c7a12fe65f43c2825ba6")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'tos_data)))
  "Returns md5sum for a message object of type 'tos_data"
  "b2965ddc92e8c7a12fe65f43c2825ba6")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<tos_data>)))
  "Returns full string definition for message of type '<tos_data>"
  (cl:format cl:nil "float32 angle~%bool modalite~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'tos_data)))
  "Returns full string definition for message of type 'tos_data"
  (cl:format cl:nil "float32 angle~%bool modalite~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <tos_data>))
  (cl:+ 0
     4
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <tos_data>))
  "Converts a ROS message object to a list"
  (cl:list 'tos_data
    (cl:cons ':angle (angle msg))
    (cl:cons ':modalite (modalite msg))
))
