#include "BornibusActions.h"

Elevator::Elevator(uint8_t position, AX12 frontAX, AX12 backAX, uint8_t frontID, uint8_t backID)
{
    _position = position;
    _frontAX = frontAX;
    _backAX = backAX;
    _frontID = frontID;
    _backID = backID;
}

void Elevator::begin(uint8_t id_front, uint8_t id_back)
{
    _backAX.attach(id_back);
    _frontAX.attach(id_front);
    _backAX.setEndlessMode(id_back);
    _frontAX.setEndlessMode(id_front);
}

void Elevator::setPosition(uint8_t position)
{
    _position = position;
}

int Elevator::getPosition()
{
    int p = _position;
    return p;
}

void Elevator::goTo(uint8_t height)
{
    //this->_frontAX.setEndlessMode(true);
    //this->_backAX.setEndlessMode(true);
    if (height==HIGH_POSITION && (this->_position != HIGH_POSITION))
    {
        this->_frontAX.turn(-500);
        this->_backAX.turn(-500);
        this->_position = MOVE_UP;   
    }
    else if (height==LOW_POSITION && (this->_position != LOW_POSITION))
    {
        this->_frontAX.turn(500);
        this->_backAX.turn(500);  
        this->_position = MOVE_DOWN;   
    }
}

void Elevator::stop()
{
    this->_frontAX.turn(0);
    this->_backAX.turn(0);
}

void Elevator::checkPosition(uint8_t pinHigh, uint8_t pinLow)
{
    if(!digitalRead(pinHigh) && (_position==MOVE_UP))
    {
        this->stop();
        _position = HIGH_POSITION;
    }
    if(!digitalRead(pinLow) && (_position==MOVE_DOWN))
    {
        this->stop();
        _position = LOW_POSITION;
    }
}

void Elevator::calibrate()
{
    _frontAX.moveSpeed(150, 100);
    _backAX.moveSpeed(150, 100);
}

Clamp::Clamp(Servo servo, uint8_t state)
{
    _servo = servo;
    _state = state;
}

void Clamp::attach(uint8_t pin)
{
    _servo.attach(pin);
}

void Clamp::close()
{
    _servo.write(closed_clamp_position);
}

void Clamp::open()
{
    _servo.write(open_clamp_position);
}

void Clamp::move(int position)
{
    _servo.write(position);
}

WindsockArm::WindsockArm(Servo armServo, uint8_t armState)
{   
    _armServo = armServo;
    _armState = armState;
}

void WindsockArm::attach(uint8_t pin)
{
    _armServo.attach(pin);
}

void WindsockArm::fold()
{
    _armServo.write(folded_windsock_arm);
}

void WindsockArm::unfold()
{
    _armServo.write(unfolded_windsock_arm);
}

void WindsockArm::end()
{
    _armServo.write(end_windsock_arm);
}

void WindsockArm::moveArm(int position)
{
    _armServo.write(position);
}

Flag::Flag(uint8_t position, AX12 flagAX, uint8_t flagID)
{
    _position = position;
    _flagAX = flagAX;
    _flagID = flagID;
}
    
void Flag::begin(uint8_t id_AX)
{
    this->_flagAX.attach(id_AX);
    this->_flagAX.setEndlessMode(true);
}
    
void Flag::setAXPosition(uint8_t position)
{
    this->_position = position;
}

int Flag::getAXPosition()
{
    return this->_position;
}

void Flag::goTo(uint8_t height)
{
    if (height==HIGH_POSITION && (this->_position != HIGH_POSITION))
    {
        this->_flagAX.turn(-1023);
        this->_position = MOVE_UP;   
    }
    else if (height==LOW_POSITION && (this->_position != LOW_POSITION))
    {
        this->_flagAX.turn(1023);
        this->_position = MOVE_DOWN;    
    }
}

void Flag::stop()
{
    _flagAX.turn(0);
}

void Flag::raiseFlag()
{
    if(this->_position != HIGH_POSITION)
    {
        this->goTo(HIGH_POSITION);
    }
}

void Flag::lowerFlag()
{
    if(this->_position != LOW_POSITION)
    {
        this->goTo(LOW_POSITION);
    }
}

void Flag::checkPosition(uint8_t pinHigh, uint8_t pinLow, WindsockArm *arm)
{
    if(!digitalRead(pinHigh) && (_position == MOVE_UP))
    {
        this->stop();
        _position = HIGH_POSITION;
        arm->end();
    }
    if(!digitalRead(pinLow) && (_position == MOVE_DOWN))
    {
        this->stop();
        _position = LOW_POSITION;
        arm->fold();
    }
}

void Flag::calibrate()
{   
    this->lowerFlag();
}