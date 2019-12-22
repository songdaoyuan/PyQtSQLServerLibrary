USE Library
CREATE TABLE TB_ReaderType(
    rdType SMALLINT PRIMARY KEY,
    rdTypeName NVARCHAR(20) NOT NULL UNIQUE,
    CanLendQty INT,
    CanLendDay INT,
    CanContinueTimes INT,
    PunishPate FLOAT,
    DateValid SMALLINT NOT NULL DEFAULT 0,
)
GO

CREATE TABLE TB_Reader(
    rdID INT PRIMARY KEY,
    rdName NVARCHAR(20),
    rdSex NCHAR(1) CHECK(rdSex IN('男','女')) DEFAULT '男',
    rdType SMALLINT REFERENCES TB_ReaderType(rdType), --CONSTRAINT FK_ReaderType_Reader FOREIGN KEY指定外键名称
    rdDept NVARCHAR(20),
    rdPhone NVARCHAR(25),
    rdEmail NVARCHAR(25),
    rdDateReg DATETIME,
    rdPhoto IMAGE,
    rdStatus NCHAR(2) CHECK(rdStatus IN('有效','挂失','注销')) DEFAULT '有效',
    rdBorrowQty INT DEFAULT 0,
    rdPwd NVARCHAR(20) DEFAULT '123',
    rdAdminRoles SMALLINT
)

CREATE TABLE TB_Book(
    bkID INT PRIMARY KEY,
    bkCode NVARCHAR(20),
    bkName NVARCHAR(50),
    bkAuthor NVARCHAR(30),
    bkPress NVARCHAR(50),
    bkDataPress DATETIME,
    bkISBN NVARCHAR(15),
    bkCatalog NVARCHAR(30),
    bkLanguage SMALLINT CHECK(bkLanguage IN(0,1,2,3,4,5)),
    bkPages INT,
    bkPrice MONEY,
    bkDateIn DATETIME,
    bkBrief TEXT,
    bkCover IMAGE,
    bkStatus NCHAR(2) CHECK(bkStatus IN('在馆','借出','遗失','变卖','销毁'))
)

CREATE TABLE TB_Borrow(
    BorrowID NUMERIC(12,0) PRIMARY KEY,
    rdID INT REFERENCES TB_Reader(rdID),
    bkID INT REFERENCES TB_Book(bkID),
    ldContinueTimes INT,    --续借次数（第一次借时，记为0）
    ldDateOut DATETIME,
    ldDateRetPlan DATETIME,
    ldDateRetAct DATETIME,
    ldOverDay INT,
    ldOverMoney MONEY,
    ldPunishMoney MONEY,
    IsHasReturn BIT DEFAULT 0,
    OperatorLend NVARCHAR(20),
    OperatorRet NVARCHAR(20)
)
