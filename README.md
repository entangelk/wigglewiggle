# 위글위글

산출물 : [위글위글 사이트 분석](https://docs.google.com/presentation/d/1vQkjJ4ZpbXQ93Z0kshkNwqHXAluf2LkIbf9y7y9aPow/edit#slide=id.p)

site : https://wiggle-wiggle.com/



## 1.개요

인터넷 상에 공개된 데이터들을 이용하여 '위글위글' 사이트에 대한 분석 / 전략을 제시한다.

## 2. 문제 확인

![매출](./docs/image/incoms.png)

```
마케팅이나 이벤트 등으로 고객의 유입은 되고 있으나 홀딩효과 미비하여 매출이 들쭉날쭉하다.
```

## 3. 매출 분석

### 매출과 뉴스 분석

![매출 뉴스](./docs/image/news_count.png)

- LDA

```
Model : sklearn.decomposition.LatentDirichletAllocation
Scoring : gensim.models.coherencemodel.CoherenceModel
```

|월|토픽|
|---------|------------|
| 2022-08 | 서비스, 매출, CU, 여름, 호텔, 굿즈, 이벤트, 선물 |
| 2022-12 | 롯데, 칠성, 국민은행, 다이어리, 마주앙, 와인 |
| 2023-02 | 밸런타인, 신규, 세트, 캐릭터, 컬래버 |
| 2023-07 | 압구정, 스토어, LG, 캐릭터, 동성, 골프, 공항철도 |
| 2023-09 | 한가위, 추석, 편의점, 팝업스토어, 코레일 |
| 2023-12 | 신세계, 패션, 팝업스토어, 크리스마스 |
| 2024-02 | BHC, 스타필드, 브랜드, 고객, 수원 |


### 매출과 Q&A

![매출 qna](./docs/image/qna_income.png)
```
매출수와 문의수를 비교하여본 결과 상호간 양의 상관관계
```

## 4. 상품 분석

<img src="./docs/image/category_product_avg.png" alt="카테고리 평균가" width="500"/> <img src="./docs/image/category_product_qna.png" alt="카테고리 qna" width="500"/>

