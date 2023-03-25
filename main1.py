#!/bin/bash

DIALOG_CANCEL=1
DIALOG_ESC=255
HEIGHT=0
WIDTH=0

# Creating function WaitingTime to add a loading screen between dialogs

function WaitingTime() {

	dialog --backtitle "CST1500 Bash Coursework" --infobox "Please wait while $1 loads" 3 40;sleep $2
	
	clear
}

# Calling infinite loop here until the user chooses to terminate the script

while true; do
	exec 3>&1
  	selection=$(dialog \
    	--backtitle "CST1500 Bash Coursework" \
    	--title "Main Menu" \
	--clear \
    	--cancel-label "Exit" \
    	--menu "Please use up/down arrow keys or mouse + click \nto move [UP/DOWN]. Return key to select" $HEIGHT $WIDTH 5 \
    	"Date/Time" "To view current date and time " \
    	"Calendar" "To view calendar" \
    	"Delete" "To delete a file" \
    	"Exit" "To exit the script" 2>&1 1>&3)
    
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
  
		Date/Time )
		
			WaitingTime "Date & Time" "2"
    
			dialog --timeout 5 --backtitle "CST1500 Bash Coursework" \
			--title "Date & Time" \
			--no-collapse \
			--clear \
			--msgbox "$(date)" 0 0
			;;
      
      
		Calendar )
    
			exec 3>&1
			selection2=$(dialog \
			--backtitle "CST1500 Bash Coursework" \
			--title "Calendar" \
			--clear \
			--menu "Select" $HEIGHT $WIDTH 3 \
			1 "View Calendar" \
			2 "Add Event to a date" 2>&1 1>&3)
			exec 3>&-
      	
			case $selection2 in
      	
			1 )
			
				WaitingTime "Calendar" "2"
      	
				Date2=$(dialog --backtitle "CST1500 Bash Coursework" \
				--title "Calendar" \
				--calendar "Select Date" 0 0 3>&1 1>&2 2>&3 3>&-)
				
				cancel_status=$?
				3>&-
				case $cancel_status in
					$DIALOG_CANCEL)
					clear
					continue
					;;
					
					$DIALOG_ESC)
					clear
					continue
					;;
				esac
      	
				#Reading the file that contains the events and the dates
    	
				while read line
				do echo $line

				clear

				date2=$(cut -d'-' -f1 <<<"$line")   

				if [ $date2 == $Date2 ]
				then
					info2=$(cut -d'-' -f2- <<<"$line")
					info3+="$info2\n"
				fi

				done < events.txt

				clear

				dialog --backtitle "CST1500 Bash Coursework" \
				--title "Calendar" \
				--msgbox "Event Info for "$Date2":\n$info3" 0 0

				unset info3

				clear
				;;

			2 )
			
				WaitingTime "Calendar" "2"
      	
				Date=$(dialog --backtitle "CST1500 Bash Coursework" \
				--title "Calendar" \
				--calendar "Select Date" 0 0 3>&1 1>&2 2>&3)
				
				cancel_status=$?
				3>&-
				case $cancel_status in
					$DIALOG_CANCEL)
					clear
					continue
					;;
					
					$DIALOG_ESC)
					clear
					continue
					;;
				esac
				
				clear
      		
				Info=$(dialog --backtitle "CST1500 Bash Coursework" \
				--title "Event info" \
				--inputbox "Enter Info" 0 0 3>&1 1>&2 2>&3)
				
				cancel_status=$?
				3>&-
				case $cancel_status in
					$DIALOG_CANCEL)
					clear
					continue
					;;
					
					$DIALOG_ESC)
					clear
					continue
					;;
				esac
      	
				# Creating a file called Events which will be created in current directory to store the info and the date
   			
				echo "$Date-$Info" >> events.txt
      	
				dialog --backtitle "CST1500 Bash Coursework" \
				--title "Info added to a file in current directory" \
				--no-collapse \
				--clear \
				--msgbox "$Date $Info" 0 0
      			
			esac
			;;
      
      
		Delete )
    
			WaitingTime "Delete" "2"
			
			dialog --backtitle "CST1500 Bash Coursework" \
			--title "Path" \
			--inputbox "Enter directory path/ Leave inputbox empty to use current working directory" 10 40  2>$(pwd)/filedirectory
			
                       cancel_status=$?
				3>&-
				case $cancel_status in
					$DIALOG_CANCEL)
					clear
					rm -f $(pwd)/filedirectory
					continue
					;;
					
					$DIALOG_ESC)
					clear
					rm -f $(pwd)/filedirectory
					continue
					;;
					
				esac
					
			# Create a temporary file named directory to store the path 
			
			mfile=`cat $(pwd)/filedirectory`
 
			# Check wether user entered a path. If not, script will consider current working directory
 
			if [ -z $mfile ]
			then
				mfile=`pwd`/*
			else
				grep "*" $(pwd)/filedirectory
				if [ $? -eq 1 ]
				then
					mfile=$mfile/*
				fi    
			fi
 
			for i in $mfile 
			do
			if [ -f $i ]
			then
				echo "$i Delete?" >> $(pwd)/filelist
			fi	
			done    

			# Menu to display and select the files like sort of a file manager ui

			dialog --backtitle "CST1500 Bash Coursework" \
			--title "Select file to delete" \
			--menu "Use [Up/Down] to move, [Enter] to select file" 20 60 12 `cat $(pwd)/filelist` 2>$(pwd)/filetodelete
 
			x=$? 
 
			# Storing the name of the file to delete selected by the user in a temporary file named filetodelete

			erase=`cat $(pwd)/filetodelete`
 
			# Confirmation box to warn and ask permission wether or not to permanently delete the selected file

			case $x in 
				0) dialog --timeout 10 --backtitle "CST1500 Bash Coursework" \
				--title "Confirmation" \
				--yesno "\n\nAre you sure want to permanently delete this file : $erase ?" 10 60
     
			# Notify user wether selected file has been successfully deleted or not

			if [ $? -eq 0 ] ; then
			
			# Progress bar that will appear while deleting file
			
                       for i in $(seq 0 20 100); 
                       do sleep 0.6; 
                       echo $i | dialog --backtitle "CST1500 Bash Coursework" --title "Deleting..." --gauge "Deleting $erase" 10 70 0; 
                       done

			rm -f  $erase         
				if [ $? -eq 0 ] ; then
					dialog --backtitle "CST1500 Bash Coursework" \
					--title "Success" \
					--infobox "File: $erase sucessfully deleted. Press Enter to go back" 5 60
					read
				else
					dialog --backtitle "CST1500 Bash Coursework" 
					--title "Error"
					--infobox "Error deleting File: $erase. Press Enter to go back" 5 60
					read       
				fi
			else
				dialog --backtitle "CST1500 Bash Coursework" \
				--title "Error" \
				--infobox "File: $erase not deleted. Press Enter to go back" 5 60
				read
			fi
			;;
     
			# Deleting temporary (tmp) files as soon as task has been completed or when user chooses to exit the script
 
			1)  	rm -f $(pwd)/filedirectory ; rm -f $(pwd)/filelist ; 
					rm -f $(pwd)/filetodelete; return;;
			255) 	rm -f $(pwd)/filedirectory ;  rm -f $(pwd)/filelist ;
					rm -f $(pwd)/filetodelete; return;;
			esac
			rm -f $(pwd)/filedirectory
			rm -f $(pwd)/filelist
			rm -f $(pwd)/filetodelete
			return
			
			;;

		Exit )
			clear
			echo "Program Terminated"; break
			;;
	esac
done
