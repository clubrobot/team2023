#include <math.h>
#include "mathutils.h"

/**
 * @brief Applique  un modulo
 * 
 * @param x 
 * @param y 
 * @return float 
 */
float periodicmod(float x, float y)
{
    return fmod(fmod(x, y) + y, y);
}

/**
 * @brief Projet la variable x dans l'intervale min, max.
 * 
 * Cette fonction est très utile pour projeter des angles sur -pi / pi par exemple.
 * 
 * @param x Variable à projeter sur un intervalle.
 * @param min Valeur basse de l'intervalle.
 * @param max Valeur haute de l'intervalle.
 * @return float Valeur bornée sur l'intervalle.
 */
float inrange(float x, float min, float max)
{
    return periodicmod(x - min, max - min) + min;
}

/**
 * @brief Borne la variable x entre les bornes.
 * 
 * @param x Variable à plaquer sur un intervalle.
 * @param min Valeur basse de l'intervalle.
 * @param max Valeur haute de l'intervalle.
 * @return float Valeur plaquée sur l'intervalle.
 */
float saturate(float x, float min, float max)
{
    if (x < min)
        return min;
    else if (x > max)
        return max;
    else
        return x;
}

/**
 * @brief Retourne l'information du signe
 * 
 * @param x Variable à extraire le signe
 * @return float 1 pour une variable positif -1 pour une négatif et 0 pour une variable nul (=0).
 */
float sign(float x)
{
    if (x < 0)
        return -1;
    else if (x > 0)
        return 1;
    else
        return 0;
}
