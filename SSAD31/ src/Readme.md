#### Description:
* super_admin :- This folder contains automation script for various features of 
                super admin role like add hospital,add staff,change password,
                edit function,deactivate function etc
                     
* doctor :- This folder contains automation script for various features of doctor
            role like manage assistants,view notifications etc
                
* admin :- This folder contains automation script for various features of 
            hospital amdin role like add staff,add patients,add articles,
            videos,view notifications etc
* cms   :- This folder contains automation script for various features of cms staff
           like add article,send messages,edit profile,change password etc
* call_center_staff :- This folder contains automation script for various featurs of
                      call center staff like view patients,change password etc
* assistant_doctor :- This folder contains automation script for various features of
                     assistant doctor like view patients,send messages etc
#### Requirements:-
* Gmail Api should be installled
  * sudo pip install --upgrade google-api-python-client
* Selenium binding should be installed to the python
  * sudo pip install selenium
* Place Geckodriver executable in the above folders

#### To run :- 
 * Intsructions for executing these auromation scripts are given in respective README files.
 * Order of execution of the files Should be :- 
   * super_admin
   * admin
   * doctor
   * assistant_doctor
   * cms
   * call_center_staff
 * Also make sure to delete the data in the databases before executing these automation scripts using Pgadmin. 