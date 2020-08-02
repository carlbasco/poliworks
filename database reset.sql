-- SQLite
delete from `construction_requisition`;    
delete from sqlite_sequence where name='`construction_requisition`';

delete from `construction_requisitiondetails`;    
delete from sqlite_sequence where name='`construction_requisitiondetails`';

delete from `construction_requisitiondelivery`;    
delete from sqlite_sequence where name='`construction_requisitiondelivery`';

delete from `construction_requisitionimage`;    
delete from sqlite_sequence where name='`construction_requisitionimage`';

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

delete from `construction_materialreport`;    
delete from sqlite_sequence where name='`construction_materialreport`';

delete from `construction_materialreportdetails`;    
delete from sqlite_sequence where name='`construction_materialreportdetails`';

delete from `construction_sitephotos`;    
delete from sqlite_sequence where name='`construction_sitephotos`';

delete from `construction_sitephotosdetails`;    
delete from sqlite_sequence where name='`construction_sitephotosdetails`';

delete from `construction_externalmaterialreport`;    
delete from sqlite_sequence where name='`construction_externalmaterialreport`';

delete from `construction_externalmaterialreportdetails`;    
delete from sqlite_sequence where name='`construction_externalmaterialreportdetails`';

delete from `construction_externalprojectinventory`;    
delete from sqlite_sequence where name='`construction_externalprojectinventory`';

delete from `construction_externalprojectinventorydetails`;    
delete from sqlite_sequence where name='`construction_externalprojectinventorydetails`';

delete from `construction_materialreportdetails`;    
delete from sqlite_sequence where name='`construction_materialreportdetails`';

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

delete from `construction_inquiry`; 
delete from sqlite_sequence where name='`construction_inquiry`';

delete from `construction_estimate`; 
delete from sqlite_sequence where name='`construction_estimate`';

delete from `construction_estimateimage`; 
delete from sqlite_sequence where name='`construction_estimateimage`';

delete from `construction_notification`; 
delete from sqlite_sequence where name='`construction_notification`';

delete from `construction_estimate`; 
delete from sqlite_sequence where name='`construction_estimate`';

delete from `construction_inquiry`; 
delete from sqlite_sequence where name='`construction_inquiry`';

delete from `construction_personneljoborder`; 
delete from sqlite_sequence where name='`construction_personneljoborder`';

delete from `construction_reworkbeforeimage`; 
delete from sqlite_sequence where name='`construction_reworkbeforeimage`';

delete from `construction_reworkafterimage`; 
delete from sqlite_sequence where name='`construction_reworkafterimage`';

delete from `construction_externalorderimage`; 
delete from sqlite_sequence where name='`construction_reworkafterimage`';

UPDATE 'construction_personnel' SET joborder_count=0 WHERE joborder_count=1;