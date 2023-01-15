;; Auto-generated. Do not edit!


(when (boundp 'raspberry::tos_data)
  (if (not (find-package "RASPBERRY"))
    (make-package "RASPBERRY"))
  (shadow 'tos_data (find-package "RASPBERRY")))
(unless (find-package "RASPBERRY::TOS_DATA")
  (make-package "RASPBERRY::TOS_DATA"))

(in-package "ROS")
;;//! \htmlinclude tos_data.msg.html


(defclass raspberry::tos_data
  :super ros::object
  :slots (_angle _modalite ))

(defmethod raspberry::tos_data
  (:init
   (&key
    ((:angle __angle) 0.0)
    ((:modalite __modalite) nil)
    )
   (send-super :init)
   (setq _angle (float __angle))
   (setq _modalite __modalite)
   self)
  (:angle
   (&optional __angle)
   (if __angle (setq _angle __angle)) _angle)
  (:modalite
   (&optional (__modalite :null))
   (if (not (eq __modalite :null)) (setq _modalite __modalite)) _modalite)
  (:serialization-length
   ()
   (+
    ;; float32 _angle
    4
    ;; bool _modalite
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _angle
       (sys::poke _angle (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; bool _modalite
       (if _modalite (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _angle
     (setq _angle (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; bool _modalite
     (setq _modalite (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get raspberry::tos_data :md5sum-) "b2965ddc92e8c7a12fe65f43c2825ba6")
(setf (get raspberry::tos_data :datatype-) "raspberry/tos_data")
(setf (get raspberry::tos_data :definition-)
      "float32 angle
bool modalite

")



(provide :raspberry/tos_data "b2965ddc92e8c7a12fe65f43c2825ba6")


