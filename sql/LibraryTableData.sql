--测试数据库的过程中需要录入的数据
USE Library
GO
--首先初始化TB_ReaderType表内数据
insert into [TB_ReaderType]	values(10,'教师',12,60,2,0.05,0);
insert into [TB_ReaderType]	values(20,'本科生',8,30,1,0.05,4);
insert into [TB_ReaderType]	values(21,'专科生',8,30,1,0.05,3);
insert into [TB_ReaderType]	values(30,'硕士研究生',8,30,1,0.05,3);
insert into [TB_ReaderType]	values(31,'博士研究生',8,30,1,0.05,4);
GO
--查看TB_ReaderType表
SELECT * FROM TB_ReaderType
GO
--Account对象内方法的核心SQL语句
--登录的SQL语句
SELECT rdAdminRoles FROM TB_Reader WHERE rdID=1 AND rdPwd=''
GO
--修改密码的SQL语句
UPDATE TB_Reader SET rdPwd='sdy317421' WHERE rdID=1
GO
--初始化TB_Book表内数据
INSERT INTO TB_Book VALUES(1,'9787115313980','SQL必知必会','Ben Forta','人民邮电出版社','2013-05-01 00:00:00','9787115313980','TP311.131',0,239,29.00,GETDATE(),'畅销全球的数据库入门经典','','在馆')
GO
--查看TB_Book表
SELECT * FROM TB_Book
GO
--清空TB_Book表
DELETE FROM TB_Book
GO
/*
TB_Book表的数据结构参考
1	bkID	Int	图书序号【标识列，主键】
2	bkCode	Nvarchar (20)	图书编号或条码号（前文中的书号）
3	bkName	Nvarchar(50)	书名
4	bkAuthor	Nvarchar(30)	作者
5	bkPress	Nvarchar(50)	出版社
6	bkDatePress	datetime	出版日期
7	bkISBN	Nvarchar (15)	ISBN书号
8	bkCatalog	Nvarchar(30)	分类号（如：TP316-21/123）
9	bkLanguage	SmallInt	语言，0-中文，1-英文，2-日文，3-俄文，4-德文，5-法文
10	bkPages	Int	页数
11	bkPrice	Money	价格
12	bkDateIn	DateTime	入馆日期
13	bkBrief	Text	内容简介
14	bkCover	image	图书封面照片
15	bkStatus	NChar(2)	图书状态，在馆、借出、遗失、变卖、销毁
*/
--初始化TB_Reader表内数据
INSERT INTO TB_Reader VALUES(1,'宋道源','男',20,'CS','15171539455','835128023@qq.com',GETDATE(),'','有效',0,'sdy2000317421',15)
INSERT INTO TB_Reader VALUES(2,'朱晨光','男',21,'CS','13349745060','841102344@qq.com',GETDATE(),'','有效',0,'123',15)
GO
--查看TB_Reader表
SELECT * FROM TB_Reader
GO