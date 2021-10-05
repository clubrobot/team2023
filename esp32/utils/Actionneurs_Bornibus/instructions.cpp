#include "instructions.h"
#include "BornibusActions.h"

#include <SerialTalks.h>

extern Elevator e1;
extern Elevator e2;
extern Elevator e3;

extern Clamp clamp0;
extern Clamp clamp1;
extern Clamp clamp2;
extern Clamp clamp3;
extern Clamp clamp4;

extern WindsockArm arm;
extern Flag sailFlag;

void MOVE_ELEVATOR(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    byte id = input.read<byte>();
    byte height = input.read<byte>();
    
    if(id == 0)
    {
        if (height == 0)
        {
            e1.goTo(LOW_POSITION);
        }
        else if (height == 1)
        {
            e1.goTo(HIGH_POSITION);
        }
    }
    else if(id == 1)
    {
        if (height == 0)
        {
            e2.goTo(LOW_POSITION);
        }
        else if (height == 1)
        {
            e2.goTo(HIGH_POSITION);
        }
    }
    else if(id == 2)
    {
        if (height == 0)
        {
            e3.goTo(LOW_POSITION);
        }
        else if (height == 1)
        {
            e3.goTo(HIGH_POSITION);
        }
    }
    else 
    {
        e3.stop();
    }
}

void GET_ELEVATOR_POSITION(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    byte id = input.read<byte>();

    if (id == 0)
    {
        output.write<byte>(e1.getPosition());
    }
    else if (id == 1)
    {
        output.write<byte>(e2.getPosition());
    }
    else if (id == 2)
    {
        output.write<byte>(e3.getPosition());
    }
    else
    {
        output.write<byte>(ERROR);
    }
}

void MOVE_CLAMP(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    byte id = input.read<byte>();
    byte state = input.read<byte>();

    if(state == 1)
    {
        switch (id)
        {
            case 0:
                clamp0.move(open_clamp0_position);
            break;
            case 1:
                clamp1.move(open_clamp1_position);
            break;
            case 2:
                clamp2.move(open_clamp2_position);
            break;
            case 3:
                clamp3.move(open_clamp3_position);
            break;
            case 4:
                clamp4.move(open_clamp4_position);
            break;
        }
    }
    else if (state == 0)
    {
        switch (id)
        {
            case 0:
                clamp0.move(closed_clamp0_position);
            break;
            case 1:
                clamp1.move(closed_clamp1_position);
            break;
            case 2:
                clamp2.move(closed_clamp2_position);
            break;
            case 3:
                clamp3.move(closed_clamp3_position);
            break;
            case 4:
                clamp4.move(closed_clamp4_position);
            break;
        }
    }

}

void SET_CLAMP_POSITION(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    byte id = input.read<byte>();
    byte position = input.read<byte>();

    switch (id)
    {
        case 0:
            clamp0.move(position);
        break;
        case 1:
            clamp1.move(position);
        break;
        case 2:
            clamp2.move(position);
        break;
        case 3:
            clamp3.move(position);
        break;
        case 4:
            clamp4.move(position);
        break;
    }   
}

void MOVE_WINDSOCK_ARM(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    byte state = input.read<byte>();

    if(state == 0)
    {
        arm.moveArm(180);
    }
    else if(state == 1)
    {
        arm.moveArm(100);
    }
    else if(state == 2);
    {
        arm.moveArm(0);
    }
}

void SET_WINDSOCK_ARM_POSITION(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    byte position = input.read<byte>();

    arm.moveArm(position);
}

void MOVE_FLAG(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    byte height = input.read<byte>();
    
    if (height == 0)
    {
        sailFlag.goTo(LOW_POSITION);
    }
    else if (height == 1)
    {
        sailFlag.goTo(HIGH_POSITION);
    }
    else 
    {
        sailFlag.stop();
    }
}

void RAISE_FLAG(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    arm.unfold();
    sailFlag.raiseFlag();
}

void LOWER_FLAG(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    arm.unfold();
    sailFlag.lowerFlag();
}

void GET_FLAG_POSITION(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    output.write<byte>(sailFlag.getAXPosition());
}

void CALIBRATE_ELEVATOR(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    byte id = input.read<byte>();

    if(id==0)
    {
        e1.calibrate();
    }
    else if(id==1)
    {
        e2.calibrate();
    }
    else if(id==2)
    {
        e3.calibrate();
    }
}

void CALIBRATE_FLAG(SerialTalks &inst, Deserializer &input, Serializer &output)
{
    sailFlag.calibrate();
}