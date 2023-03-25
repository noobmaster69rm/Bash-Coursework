#!/bin/bash

# while-menu-dialog: a menu driven system information program

DIALOG_CANCEL=1
DIALOG_ESC=255
HEIGHT=0
WIDTH=0

# Creating function WaitingTime to add a loading screen between dialogs

function WaitingTime() {

	dialog --backtitle "CST1500 Bash Coursework" --infobox "Please wait while $1 loads" 3 50;sleep $2
	
	clear
}

# Pre assigned variable that will display the backtitle, title and message box without wrapping texts together

display_result() {
  dialog --backtitle "CST1500 Bash Coursework" \
    --title "$1" \
    --no-collapse \
    --msgbox "$result" 0 0
}

# calling infinite loop here until the user chooses to terminate the script

while true
do
exec 3>&1
selection=$(dialog \
    --backtitle "CST1500 Bash Coursework" \
    --title "Main Menu" \
    --clear \
    --cancel-label "Exit" \
    --menu "Please use up/down arrow keys or mouse + click to move [UP/DOWN]. Return key to select" $HEIGHT $WIDTH 6 \
    "OS-Type" "Display type of Operating System" \
    "CPU-Info" "Display Information about CPU" \
    "Memory-Info" "DIsplay Memory Information" \
    "HardDisk-Info" "Display Hard Disk Information" \
    "File-Systems" "Display Information About Mounted File Systems" 2>&1 1>&3)
    
  exit_status=$?
  exec 3>&-
  case $exit_status in
    $DIALOG_CANCEL)
      clear
      echo "Program terminated."
      exit
      ;;
    $DIALOG_ESC)
      clear
      echo "Program aborted." >&2
      exit 1
      ;;
  esac
  case $selection in
  
    OS-Type )
    
      WaitingTime "OS Type" "2"
      
      result=$(cat /etc/os-release)
      display_result "Operating System Type"
      ;;
      
      
    CPU-Info )
    
      WaitingTime "CPU Info" "2"
      
      result=$(cat /proc/cpuinfo)
      display_result "CPU Information"
      ;;
      
      
    Memory-Info )
    
      WaitingTime "Memory Info" "2"
      
      result=$(cat /proc/meminfo)
      display_result "Memory Information"
      ;;
      
      
    HardDisk-Info )
    
      WaitingTime "Hard Disk Info" "2"
      
      result=$(lsblk /dev/sda)
      display_result "Hard Disk Information"
      ;;
      
      
    File-Systems )
    
    WaitingTime "Mounted File Systems" "2"
      df
      result=$(df -H)
      display_result "Mounted File System(s)"
      ;;
      
  esac
done
