#!/usr/bin/env bash
# Simple backup with rsync
# local-mode, tossh-mode, fromssh-mode

SOURCES=(/root /etc /home /boot )
TARGET="/media/nas/backup"

# edit or comment with "#"
LISTPACKAGES=listdebianpackages        # local-mode and tossh-mode
MONTHROTATE=monthrotate                 # use DD instead of YYMMDD

RSYNCCONF=(--delete)
MOUNTPOINT="/media/nas/"               # check local mountpoint
#MAILREC="user@domain"

#SSHUSER="sshuser"
#FROMSSH="fromssh-server"
#TOSSH="tossh-server"
SSHPORT=22


service --status-all

### do not edit ###

LAST="last"; INC="--link-dest=$TARGET/$LAST"
INC="--link-dest=$TARGET/$LAST"

LOG=$0.log
date > $LOG

if [ "${TARGET:${#TARGET}-1:1}" != "/" ]; then
  TARGET=$TARGET/
fi

if [ "$LISTPACKAGES" ] && [ -z "$FROMSSH" ]; then
  echo "dpkg --get-selections | awk '!/deinstall|purge|hold/'|cut -f1 | tr '\n' ' '" >> $LOG
  dpkg --get-selections | awk '!/deinstall|purge|hold/'|cut -f1 |tr '\n' ' '  >> $LOG  2>&1
fi

if [ "$MOUNTPOINT" ]; then
  MOUNTED=$(mount | fgrep "$MOUNTPOINT");
fi

if [ -z "$MOUNTPOINT" ] || [ "$MOUNTED" ]; then
  if [ -z "$MONTHROTATE" ]; then
    TODAY=$(date +%y%m%d)
  else
    TODAY=$(date +%d)
  fi

  if [ "$SSHUSER" ] && [ "$SSHPORT" ]; then
    S="ssh -p $SSHPORT -l $SSHUSER";
  fi

  for SOURCE in "${SOURCES[@]}"
    do
      if [ "$S" ] && [ "$FROMSSH" ] && [ -z "$TOSSH" ]; then
        echo "rsync -e \"$S\" -avR \"$FROMSSH:$SOURCE\" ${RSYNCCONF[@]} $TARGET$TODAY $INC"  >> $LOG
        rsync -e "$S" -avR "$FROMSSH:\"$SOURCE\"" "${RSYNCCONF[@]}" "$TARGET"$TODAY $INC >> $LOG 2>&1
        if [ $? -ne 0 ]; then
          ERROR=1
        fi
      fi
      if [ "$S" ]  && [ "$TOSSH" ] && [ -z "$FROMSSH" ]; then
        echo "rsync -e \"$S\" -avR \"$SOURCE\" ${RSYNCCONF[@]} \"$TOSSH:$TARGET$TODAY\" $INC " >> $LOG
        rsync -e "$S" -avR "$SOURCE" "${RSYNCCONF[@]}" "$TOSSH:\"$TARGET\"$TODAY" $INC >> $LOG 2>&1
        if [ $? -ne 0 ]; then
          ERROR=1
        fi
      fi
      if [ -z "$S" ]; then
        echo "rsync -avR \"$SOURCE\" ${RSYNCCONF[@]} $TARGET$TODAY $INC"  >> $LOG
        rsync -avR "$SOURCE" "${RSYNCCONF[@]}" "$TARGET"$TODAY $INC  >> $LOG 2>&1
        if [ $? -ne 0 ]; then
          ERROR=1
        fi
      fi
  done

  if [ "$S" ] && [ "$TOSSH" ] && [ -z "$FROMSSH" ]; then
    echo "ssh -p $SSHPORT -l $SSHUSER $TOSSH ln -nsf $TARGET$TODAY $TARGET$LAST" >> $LOG
    ssh -p $SSHPORT -l $SSHUSER $TOSSH "ln -nsf \"$TARGET\"$TODAY \"$TARGET\"$LAST" >> $LOG 2>&1
    if [ $? -ne 0 ]; then
      ERROR=1
    fi
  fi
  if ( [ "$S" ] && [ "$FROMSSH" ] && [ -z "$TOSSH" ] ) || ( [ -z "$S" ] );  then
    echo "ln -nsf $TARGET$TODAY $TARGET$LAST" >> $LOG
    ln -nsf "$TARGET"$TODAY "$TARGET"last  >> $LOG 2>&1
    if [ $? -ne 0 ]; then
      ERROR=1
    fi
  fi
else
  echo "$MOUNTPOINT not mounted" >> $LOG
  ERROR=1
fi
date >> $LOG
if [ -n "$MAILREC" ]; then
  if [ $ERROR ];then
    mail -s "Error Backup $LOG" $MAILREC < $LOG
  else
    mail -s "Backup $LOG" $MAILREC < $LOG
  fi
fi