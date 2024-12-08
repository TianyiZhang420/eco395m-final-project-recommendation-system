import http.client
import json
import csv
import time

# 设置 API 连接和请求头
conn = http.client.HTTPSConnection("sephora14.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "60bc1d8728msh735d4cfdb538423p1f40d0jsn42655b7e4794",  # 替换为你的 RapidAPI Key
    'x-rapidapi-host': "sephora14.p.rapidapi.com"
}

# 读取 product_info.csv 文件中的 ProductId
def read_product_ids(csv_file):
    product_ids = []
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            product_ids.append(row["productId"])
    return product_ids

# 提取 ContextDataValues 中的字段值
def extract_context_values(context_data):
    # 需要提取的字段
    result = {
        "skinTone": "",
        "eyeColor": "",
        "skinType": "",
        "IncentivizedReview": "",
        "hairColor": ""
    }
    
    # 检查 context_data 是否是字典
    if isinstance(context_data, dict):
        for key in result.keys():
            # 如果 context_data 中包含该字段，则提取其中的 'Value' 字段
            if key in context_data:
                value_data = context_data[key]
                if isinstance(value_data, dict) and "Value" in value_data:
                    result[key] = value_data["Value"]  # 提取 'Value' 字段的值
    
    return result

# 获取每个产品的评论数据
def fetch_reviews_for_product(product_id, limit=50):
    offset = 0  # 数据偏移量
    all_reviews = []  # 存储所有评论
    
    # 只需要获取一页评论，每页 100 条
    url = f"/productReviews?productID={product_id}&page=1"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()

    response_data = data.decode("utf-8")
    #print(response_data)
    # 解析 JSON 数据
    json_data = json.loads(response_data)
    
    if isinstance(json_data, list):
        results = json_data  # 直接使用 json_data 作为评论数据
    else:
        results = json_data.get("Results", [])  # 如果是字典，提取 "Results" 键
   
    #print(results)
    
    # 如果没有更多数据，返回空列表
    if not results:
        print(f"所有 {product_id} 的评论已获取完成！")
        return []

    # 处理每条评论并提取需要的数据，最多取 50 条评论
    for review in results[:limit]:  # 只取前 50 条评论
        context_values = extract_context_values(review.get("ContextDataValues", {}))
        all_reviews.append({
            #"Id": review.get("Id", ""),
            "ProductId": product_id,  # 使用 CSV 文件中的 productId 替代 API 返回的 ProductId
            "OriginalProductName": review.get("OriginalProductName", ""),
            "Rating": review.get("Rating", ""),
            "Helpfulness": review.get("Helpfulness", ""),
            "ReviewText": review.get("ReviewText", ""),
            "Title": review.get("Title", ""),
            "skinTone": context_values.get("skinTone", ""),
            "eyeColor": context_values.get("eyeColor", ""),
            "skinType": context_values.get("skinType", ""),
            "hairColor": context_values.get("hairColor", "")
        })

    print(f"获取了 {len(all_reviews)} 条评论")
    return all_reviews

# 将评论数据保存为 CSV 文件
def save_reviews_to_csv(reviews, output_file="data/review.csv"):
    csv_headers = ["ProductId", "OriginalProductName", "Rating", "ReviewText", "Title", 
                   "Helpfulness", "skinTone", "eyeColor", "skinType","hairColor"]
    
    with open(output_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)
        writer.writeheader()  # 写入 CSV 文件头

        for review in reviews:
            writer.writerow(review)
    
    print(f"数据已保存至 {output_file}，共保存了 {len(reviews)} 条评论。")

# 主函数
def main():
    product_ids = read_product_ids("data/category_product_new.csv")  # 从文件读取 ProductId
    all_reviews = []

    for idx, product_id in enumerate(product_ids):
        print(f"正在获取产品 {product_id} 的评论...")
        product_reviews = fetch_reviews_for_product(product_id)
        all_reviews.extend(product_reviews)
        print(f"Fetched {len(product_reviews)} reviews for product {product_id}")

        # 每爬取 20 个产品后保存一次评论数据
        if (idx + 1) % 20 == 0:
            save_reviews_to_csv(all_reviews, output_file="data/review.csv")

        # 每次请求后暂停 1 秒，以遵守每秒一个请求的限制
        time.sleep(1)

    # 如果循环结束时还有剩余评论，保存它们
    if all_reviews:
        save_reviews_to_csv(all_reviews, output_file="data/review.csv")

    #product_ids = read_product_ids("category_product_new.csv")  # 从文件读取 ProductId
    #all_reviews = []

    #for product_id in product_ids:
        #print(f"正在获取产品 {product_id} 的评论...")
       # product_reviews = fetch_reviews_for_product(product_id)
       # print(f"Fetched {len(product_reviews)} reviews for product {product_id}")
       # all_reviews.extend(product_reviews)
        
        # 每次请求后暂停 1 秒，以遵守每秒一个请求的限制
        #time.sleep(1)

    save_reviews_to_csv(all_reviews)  # 保存所有评论数据
    #print("First two product IDs:")
    #print(product_ids[:2])  # 打印前两行的 ProductId

    # 如果想测试获取评论数据的功能，可以测试前两个产品ID
    #for product_id in product_ids[:1]:
        #print(f"正在获取产品 {product_id} 的评论...")
        #product_reviews = fetch_reviews_for_product(product_id)
        #print(f"Fetched {len(product_reviews)} reviews for product {product_id}")
    #save_reviews_to_csv(product_reviews, output_file="data/test.csv")

# 执行主函数
if __name__ == "__main__":
    main()
