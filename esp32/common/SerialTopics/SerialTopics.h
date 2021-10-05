#ifndef __SERIALTOPICS_H__
#define __SERIALTOPICS_H__

#include <Arduino.h>
#include "SerialTalks.h"

#define SERIALTOPICS_DEFAULT_TIMING 100 //ms

#define SERIALTOPICS_MAX_OPCODE 5

#define MANAGE_OPCODE (SERIALTALKS_RESEVED_OPCODE_7)

#define SUBSCRIBE 0X0
#define UNSUBSCRIBE 0X1

class SerialTopics
{
public:
    /**
     * @brief Subscription function pointer
     */
    typedef void (*Subscription)(Serializer &output);

    /**
     * @brief Subscription context structure
     */
    typedef struct
    {
        /* data */
        Subscription func; /* binded function */
        long timestep;     /* timestep in ms */
        long lasttime;     /* last iteration time */
        bool enable;       /* enable /disable */
    } subscription_t;

    void begin(SerialTalks &talks);
    void bind(byte opcode, Subscription subscription);
    bool execute();

    subscription_t *getSubscriptions() { return _subscriptions; }

private:
    SerialTalks *_talks;

    subscription_t _subscriptions[SERIALTOPICS_MAX_OPCODE]; /*!< Listes des souscriptions enregistrées avec un OPCode associé.*/

    static void MANAGE(SerialTalks &talks, Deserializer &input, Serializer &output);

    static void DEFAULT_HANDLER(Serializer &output);
};

extern SerialTopics topics;

#endif // __SERIALTOPICS_H__