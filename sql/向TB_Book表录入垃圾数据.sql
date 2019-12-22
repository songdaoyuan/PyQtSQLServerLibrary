USE Library
SELECT * FROM TB_Book
INSERT INTO TB_Book VALUES(24,0000000000000,'时间简史','史蒂芬霍金','测试出版社1',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(25,0000000000001,'C++从入门到精通','测试作者','测试出版社2',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(4,0000000000002,'Python Cookbook','Nobody','测试出版社3',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(5,0000000000003,'测试图书4','测试作者4','测试出版社4',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(6,0000000000004,'测试图书5','测试作者5','测试出版社5',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(7,0000000000005,'测试图书6','测试作者6','测试出版社6',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(8,0000000000006,'测试图书7','测试作者7','测试出版社7',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(9,0000000000007,'测试图书8','测试作者8','测试出版社8',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(10,0000000000008,'测试图书9','测试作者9','测试出版社9',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(11,0000000000009,'测试图书10','测试作者10','测试出版社10',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(12,0000000000010,'测试图书11','测试作者11','测试出版社11',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(13,0000000000011,'测试图书12','测试作者12','测试出版社12',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(14,0000000000012,'测试图书13','测试作者13','测试出版社13',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(15,0000000000013,'测试图书14','测试作者14','测试出版社14',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(16,0000000000014,'测试图书15','测试作者15','测试出版社15',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(17,0000000000015,'测试图书16','测试作者16','测试出版社16',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(18,0000000000016,'测试图书17','测试作者17','测试出版社17',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(19,0000000000017,'测试图书18','测试作者18','测试出版社18',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(20,0000000000018,'测试图书19','测试作者19','测试出版社19',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(21,0000000000019,'测试图书20','测试作者20','测试出版社20',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(22,0000000000020,'测试图书21','测试作者21','测试出版社21',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
INSERT INTO TB_Book VALUES(23,0000000000021,'测试图书22','测试作者22','测试出版社22',GETDATE(),0000000000000,'TP311.131',0,239,29.0,GETDATE(),'测试简介','','在馆')
GO
declare @m int = 10
declare @n int = 12
select top (@m)  * from (select top (@n)  * from TB_Book order by bkID) as a
GO
declare @m int = 2;--从2开始，往后8条数据
declare @n int = 8;
select top (8) * from TB_Book  where bkID not in(select top (0) bkID from TB_Book) ORDER BY bkID
select top (8) * from TB_Book  where bkID not in(select top (0) bkID from TB_Book) ORDER BY bkName
USE Library
SELECT * FROM TB_Reader

SELECT * FROM TB_Book WHERE bkName LIKE '%测试%' ORDER BY bkName 
SELECT * FROM TB_Book WHERE bkAuthor LIKE '%测试%' ORDER BY bkAuthor
select top (10) * from TB_Book  where bkAuthor LIKE '%测试%' and bkID not in (select top (0) bkID from TB_Book where bkAuthor LIKE '%测试%') ORDER BY bkAuthor
SELECT * FROM TB_Book WHERE bkId=1