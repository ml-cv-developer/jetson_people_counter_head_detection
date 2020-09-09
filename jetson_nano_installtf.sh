# Step 1 : install package 
echo "------------------------------------------------------------------"
echo " 				Install 			"
echo "------------------------------------------------------------------"
sudo apt update -y
sudo apt-get install git cmake -y
sudo apt-get install libatlas-base-dev gfortran -y
sudo apt-get install libhdf5-serial-dev hdf5-tools -y
sudo apt-get install python3-dev -y
sudo apt-get install libgeos-dev -y

sudo apt-get install python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip -y

sudo apt-get install gfortran -y 
sudo apt-get install libmysqlclient-dev -y
sudo apt-get install libblas-dev  liblapack-dev -y 
sudo apt-get install python3-tk -y 

sudo apt-get install python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip -y 


# Step 2 : install virtualenv 
sudo apt install python3-dev python3-pip -y
sudo pip3 install -U virtualenv
virtualenv --system-site-packages -p python3 ./venv
# virtualenv --system-site-packages -p /usr/local/bin/python3.5 ./venv
source ./venv/bin/activate
pip install --upgrade pip

pip install --upgrade cython


     

sudo python3.6 -m pip install --upgrade cython -y

echo "------------------------------------------------------------------"
echo " 				Install Package			"
echo "------------------------------------------------------------------"
sudo apt-get install libhdf5-serial-dev hdf5-tools -y
sudo apt-get install python3-pip -y
pip3 install -U pip
sudo apt-get install zlib1g-dev zip libjpeg8-dev libhdf5-dev -y
sudo apt-get install python3-dev libmysqlclient-dev -y
sudo pip3 install -U numpy grpcio absl-py py-cpuinfo psutil portpicker grpcio six mock requests gast h5py astor termcolor

# pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v42 tensorflow-gpu
# pip install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v42 tensorflow-gpu==1.13.1+nv19.3



# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------





# Step 3: install opencv 

./install_opencv3.4.0_Nano.sh ./

# Step 4 :install package python 
pip install -r 	requirements.txt