#  ##### BEGIN GPL LICENSE BLOCK #####
# 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

def CheckPrime(num):
    """
    Checks if a integer n is prime.
    :param num: A number.
    :return: Boolean specifying whether the number is prime.
    """
    if num <= 1:
        return False
    
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            return False
    return True

def FindFactors(num, sort=False):
    """
    Finds all factors of a number.
    :param num: Number to find factors.
    :param sort=False: Whether to return factors sorted.
    :return: set of all factors.
    """
    factors = []
    for i in range(1, int(num**0.5)+1):
        if num % i == 0:
            factors.append(i)
            factors.append(num//i)
    
    if sort:
        return sorted(set(factors))
    else:
        return set(factors)