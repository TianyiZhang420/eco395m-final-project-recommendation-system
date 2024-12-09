
CREATE TABLE product_info (
    categoryID VARCHAR,
    brandName VARCHAR,
    displayName VARCHAR,
    heroImage TEXT,
    productId VARCHAR PRIMARY KEY,
    rating FLOAT,
    reviews INTEGER,
    longDescription TEXT,
    brandID VARCHAR,
    ingredientDesc TEXT,
    listPrice NUMERIC,
    quickLookDescription TEXT,
    lovesCount FLOAT,
    fullSiteProductUrl TEXT
);

 CREATE TABLE IF NOT EXISTS product_reviews (
        ProductId VARCHAR(255),  
        OriginalProductName TEXT,         
        Rating INTEGER,                  
        ReviewText TEXT,                 
        Title TEXT,                      
        Helpfulness FLOAT,             
        skinTone TEXT,                   
        eyeColor TEXT,                 
        skinType TEXT,                  
        hairColor TEXT,                 
                
    );
