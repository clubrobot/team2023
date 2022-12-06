
(cl:in-package :asdf)

(defsystem "raspberry-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "tos_data" :depends-on ("_package_tos_data"))
    (:file "_package_tos_data" :depends-on ("_package"))
  ))