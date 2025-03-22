#!/bin/bash

echo "Retail Sales Data Analysis"
echo "========================="
echo
echo "Choose an analysis to run:"
echo "1. Basic Sales Analysis"
echo "2. Advanced Sales Analysis"
echo "3. Run Both Analyses"
echo "4. Exit"
echo

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo
        echo "Running Basic Sales Analysis..."
        python simple_dashboard.py
        ;;
    2)
        echo
        echo "Running Advanced Sales Analysis..."
        python simple_advanced_analysis.py
        ;;
    3)
        echo
        echo "Running Basic Sales Analysis..."
        python simple_dashboard.py
        echo
        echo "Running Advanced Sales Analysis..."
        python simple_advanced_analysis.py
        ;;
    4)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Please try again."
        ;;
esac

echo
echo "Press Enter to exit..."
read 