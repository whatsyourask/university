#!/bin/bash

if [[ (-z $1) || (-z $2) || (-z $3) || (-z $4) ]]
then
	printf "\nUsage:\n\t./lab1_solver.sh <username1> <username2> <username3> <folder-name>\n\n"
	exit
fi

user1=$1
user2=$2
user3=$3
folder=$4

# Create 3 users
useradd $user1
useradd $user2
useradd $user3

group1="${user1}_${user2}"
group2="${user2}_${user3}"
group3="${user1}_${user3}"

# Create new groups
groupadd $group1
groupadd $group2
groupadd $group3


# Add user1 and user2 to a new group
groupmems -g $group1 -a $user1
groupmems -g $group1 -a $user2
printf "Members of group $group1:\n"
groupmems -g $group1 -l

# Add user2 and user3 to a new group
groupmems -g $group2 -a $user2
groupmems -g $group2 -a $user3
printf "Members of group $group2:\n"
groupmems -g $group2 -l

# Add user1 and user3 to a new group
groupmems -g $group3 -a $user1
groupmems -g $group3 -a $user3
printf "Members of group $group3:\n"
groupmems -g $group3 -l

# Configuring PAM for nice passwords policy
pam_passwd_file=/etc/pam.d/passwd

# Add policy about upper|lower case, digits, punctuation chars
echo "password   requisite	pam_pwquality.so minlen=11 lcredit=0 ucredit=1 dcredit=-1 ocredit=-1" >> $pam_passwd_file

# Add policy to store the history of old password for each user
echo "password   required	pam_pwhistory.so remember=400 use_authtok" >> $pam_passwd_file

# Add policy about expiration of passwords
echo "password   sufficient	pam_unix.so sha512 shadow use_authtok" >> $pam_passwd_file

login_defs=/etc/login.defs

# Change min days from 0 to 30
sed -n "s/PASS_MIN_DAYS\t0/PASS_MIN_DAYS\t30/g" $login_defs

# Change max days from 30 to 90
sed -n "s/PASS_MAX_DAYS\t30/PASS_MAX_DAYS\t90/g" $login_defs

# Change min pass len from 8 to 10
sed -n "s/PASS_MIN_LEN\t8/PASS_MIN_LEN\t10/g" $login_defs

# Make directory /$folder and create 3 files inside
mkdir -p /$folder
chmod 777 /$folder
cd /$folder
touch file1 file2 file3

# Configure the first one
chown $user1 file1
chgrp $group2 file1
chmod 640 file1

# The second
chown $user2 file2
chgrp $group3 file2
chmod 020 file2

# The third
chown $user3 file3
chgrp $group1 file3
chmod 670 file3

# Configure rsyslog to send messages to /$folder/messages and /var/log/security1
systemctl start rsyslog.service
echo "*.* /$folder/messages" > /etc/rsyslog.d/$folder.conf
echo "*.* /var/log/security1" >> /etc/rsyslog.d/$folder.conf 
# Configure SElinux for rsyslog to be able to write inside $folder
semanage fcontext -a -t var_log_t "/$folder"
restorecon -v "/${folder}"
