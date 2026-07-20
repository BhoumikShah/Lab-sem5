#!/bin/bash
# -----------------------------------------------------
# Shell Script: Arithmetic Operations
# -----------------------------------------------------

echo "Enter first number:"
read num1
echo "Enter second number:"
read num2

echo "-----------------------------------------"
echo "Menu of Arithmetic Operations"
echo "1. Addition"
echo "2. Subtraction"
echo "3. Multiplication"
echo "4. Division"
echo "5. Modulus"
echo "6. Perform ALL operations"
echo "-----------------------------------------"
echo "Enter your choice (1-6):"
read choice

case $choice in
    1)
        result=$((num1 + num2))
        echo "Addition: $num1 + $num2 = $result"
        ;;
    2)
        result=$((num1 - num2))
        echo "Subtraction: $num1 - $num2 = $result"
        ;;
    3)
        result=$((num1 * num2))
        echo "Multiplication: $num1 * $num2 = $result"
        ;;
    4)
        if [ $num2 -eq 0 ]; then
            echo "Error: Division by zero is not allowed."
        else
            result=$((num1 / num2))
            echo "Division: $num1 / $num2 = $result"
        fi
        ;;
    5)
        if [ $num2 -eq 0 ]; then
            echo "Error: Modulus by zero is not allowed."
        else
            result=$((num1 % num2))
            echo "Modulus: $num1 % $num2 = $result"
        fi
        ;;
    6)
        echo "Addition: $num1 + $num2 = $((num1 + num2))"
        echo "Subtraction: $num1 - $num2 = $((num1 - num2))"
        echo "Multiplication: $num1 * $num2 = $((num1 * num2))"
        if [ $num2 -eq 0 ]; then
            echo "Division/Modulus: Cannot divide by zero"
        else
            echo "Division: $num1 / $num2 = $((num1 / num2))"
            echo "Modulus: $num1 % $num2 = $((num1 % num2))"
        fi
        ;;
    *)
        echo "Invalid choice! Please enter a number between 1 and 6."
        ;;
esac
