use crimemap;

CREATE TABLE IF NOT EXISTS crimemap.Measure (
     measureid int NOT NULL AUTO_INCREMENT,
     rawdataid int,
     data VARCHAR(100),
     deviceid VARCHAR(100),
     createdate TIMESTAMP,
     PRIMARY KEY (measureid)
     );

CREATE TABLE IF NOT EXISTS crimemap.MeasureRaw  (
     rawdataid int NOT NULL AUTO_INCREMENT,
     rawdata VARCHAR(100),
     patientid int,
     whicheye  boolean not null default 0,
     createdate TIMESTAMP,
     PRIMARY KEY (rawdataid)
     );

CREATE TABLE IF NOT EXISTS crimemap.Patient_User   (
     patientid int ,
     userid int,
      createdate TIMESTAMP,
     PRIMARY KEY (patientid, userid)
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

/* 
insert test data:
     
insert Measure(rawdataid, data, deviceid,createdate) values(0,'250,151,152,153','88DAC8E9-08E5-81E5-D7AB-182B79D30698', now());
insert MeasureRaw(rawdata, patientid, whicheye,createdate) values('250,151,152,153',0, false, now());
insert MeasureRaw(rawdata, patientid, whicheye,createdate) values('251,151,152,153',0, true, now());
insert MeasureRaw(rawdata, patientid, whicheye,createdate) values('252,151,152,153',1, false, now());
insert MeasureRaw(rawdata, patientid, whicheye,createdate) values('253,151,152,153',1, true, now());
insert MeasureRaw(rawdata, patientid, whicheye,createdate) values('254,151,152,153',2, false, now());
insert MeasureRaw(rawdata, patientid, whicheye,createdate) values('255,151,152,153',2, true, now());
insert Patient_User(patientid, userid, createdate) values(0,0,now());
insert Patient_User(patientid, userid, createdate) values(1,0,now());
insert Patient_User(patientid, userid, createdate) values(2,1,now());

*/

