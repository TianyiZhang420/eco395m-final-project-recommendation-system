query_1 = """SELECT DISTINCT categoryid
FROM product_info
WHERE categoryid IS NOT NULL;"""

query_2 = """SELECT 
    MAX(listprice) AS maxprice,
    MIN(listprice) AS minprice
FROM 
    product_info;"""

query_3 = """SELECT DISTINCT skintype
FROM product_reviews
WHERE skintype IS NOT NULL;"""

query_4 = """SELECT DISTINCT skintone
FROM product_reviews
WHERE skintone IS NOT NULL;"""

query_5 = """SELECT 
    p.categoryid,
    p.brandname,
    p.displayname,
    p.heroimage,
    p.productid,
    p.ingredientdesc,
    p.listprice,
    p.longdescription,
    p.quicklookdescription,
    p.rating AS productrating,
    r.reviewtext,
    r.title,
    r.rating AS userrating,    
    r.helpfulness,
    r.skintone,
    r.skintype
FROM 
    product_info p
INNER JOIN 
    product_reviews r
ON 
    p.productid = r.productid
WHERE 
    p.categoryid = :category
    AND p.listprice >= :min_price
    AND p.listprice <= :max_price;"""
