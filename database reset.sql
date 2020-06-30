delete from `construction_requisition`;    
delete from sqlite_sequence where name='`construction_requisition`';

delete from `construction_requisitiondetails`;    
delete from sqlite_sequence where name='`construction_requisitiondetails`';

delete from `construction_projectinventory`;    
delete from sqlite_sequence where name='`construction_projectinventory`';

delete from `construction_projectinventorydetails`;    
delete from sqlite_sequence where name='`construction_projectinventorydetails`';

delete from `construction_externalorder`;    
delete from sqlite_sequence where name='`construction_externalorder`';

delete from `construction_externalorderdetails`;    
delete from sqlite_sequence where name='`construction_externalorderdetails`';

delete from `construction_joborder`;    
delete from sqlite_sequence where name='`construction_joborder`';

delete from `construction_jobordertask`;    
delete from sqlite_sequence where name='`construction_jobordertask`';

delete from `construction_rework`;    
delete from sqlite_sequence where name='`construction_rework`';

delete from `construction_projectdailyreport`;    
delete from sqlite_sequence where name='`construction_projectdailyreport`';

delete from `construction_sitephotos`;    
delete from sqlite_sequence where name='`construction_sitephotos`';

delete from `construction_sitephotosdetails`;    
delete from sqlite_sequence where name='`construction_sitephotosdetails`';

delete from `construction_externalorderreport`;    
delete from sqlite_sequence where name='`construction_externalorderreport`';

delete from `construction_externalorderdetailsreport`;    
delete from sqlite_sequence where name='`construction_externalorderdetailsreport`';

delete from `construction_externalprojectinventory`;    
delete from sqlite_sequence where name='`construction_externalprojectinventory`';

delete from `construction_externalprojectinventorydetails`;    
delete from sqlite_sequence where name='`construction_externalprojectinventorydetails`';

delete from `construction_projectissues`;    
delete from sqlite_sequence where name='`construction_projectissues`';

delete from `construction_quotation`;    
delete from sqlite_sequence where name='`construction_quotation`';

delete from `construction_quotationdetails`;    
delete from sqlite_sequence where name='`construction_quotationdetails`';

delete from `construction_projectprogress`;    
delete from sqlite_sequence where name='`construction_projectprogress`';

delete from `construction_projectprogressdetails`;    
delete from sqlite_sequence where name='`construction_projectprogressdetails`';

delete from `construction_projectsite`;    
delete from sqlite_sequence where name='`construction_projectsite`';

delete from `construction_projectdailyreportdetails`;    
delete from sqlite_sequence where name='`construction_projectdailyreportdetails`';

delete from `construction_personneltype`; 
delete from sqlite_sequence where name='`construction_personneltype`';

Update 'construction_personnel' SET projectsite_id=NULL, date=NULL, date2=NULL, status="Available" WHERE status = "Currently Assigned"