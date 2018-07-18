

class sd:

    def __init__(self,device):
        self.device = device

    def get_stream(self):
        raise Exception("NotImplementedException")
        #return ["dd", "..."]
# Create a filename with datestamp for our current backup (without .img suffix)
#ofile="/mnt/usb/backup_$(date +%d-%b-%y_%T)"

# Create final filename, with suffix
#ofilefinal=$ofile.img

# Begin the backup process, should take about 1 hour from 8Gb SD card to HDD
#sudo dd if="/dev/mmcblk0" of=$ofile bs=1M

# Collect result of backup procedure
#result=$?

# If command has completed successfully, delete previous backups and exit
#if [ $result=0 ]; then rm -f /mnt/usb/backup_*.img; mv $ofile $ofilefinal; exit 0;fi

#If command has failed, then delete partial backup file
#if [ $result=1 ]; then rm -f $ofile; exit 1;fi