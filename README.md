# SimpleImageCrop

간단한 이미지 크롭 프로그램을 개발했어요.

폴더를 불러와서 폴더 안에 있는 이미지들을 같은 크기로 자를 수 있어요.

자르는 영역을 쉽게 확인할 수 있고 한번에 여러 이미지들을 처리할 수 있다는 것이 장점입니다!

<img width="500" alt="image" src="https://github.com/xpile98/SimpleImageCrop/assets/19896491/9e4f5f1d-6643-48ac-a53c-3e488b289406">


## 다운로드

https://github.com/xpile98/SimpleImageCrop/blob/main/dist/SimpleImageCrop.exe

위 경로에 들어가서 프로그램을 다운받아주세요 ^^

![image](https://github.com/xpile98/SimpleImageCrop/assets/19896491/912b83d8-b802-48da-8701-0893224147ac)


## 기능 설명

* 폴더 선택
  * 크롭할 이미지가 들어있는 폴더 선택
* Width
  * 크롭할 크기 지정 (가로)
* Height
  * 크롭할 크기 지정 (세로)
* 중심 좌표 지정
  * 이미지 중심
    * 이미지 중심을 기준으로 크롭
  * 이미지 중심 + offset
    * 이미지 중심을 기준으로 크롭하되, offset 지정 가능
  * 절대 좌표
    * 좌상단을 (0,0)으로 두고 크롭할 위치를 직접 지정 가능
* 크롭
  * 크롭 동작 (**선택한 폴더_crop** 이름의 새 폴더에 저장됨)
* 이미지 뷰어
  * 폴더 내 이미지를 넘겨가며 crop 될 위치를 확인 가능

    

## 사용 예

예시를 위해 Kaggle에서 피스타치오 데이터셋을 가져와봤어요.

<img width="500" alt="image" src="https://github.com/xpile98/SimpleImageCrop/assets/19896491/4f4f0e0a-d524-4c52-812f-bade675bfdd9">

피스타치오의 좀 더 중심 부분만 집중적으로 Training 하고 싶다면, 모든 이미지에 대해서 크롭을 진행해야 하죠

300 x 300 size로 크롭하는 다양한 예를 보여드리겠습니다

1. 이미지 중심
<img width="400" alt="image" src="https://github.com/xpile98/SimpleImageCrop/assets/19896491/c3328972-be39-4459-ab58-61a4963c6095">

2. 이미지 중심 + offset (100,100)
<img width="400" alt="image" src="https://github.com/xpile98/SimpleImageCrop/assets/19896491/507f5eeb-0da5-4cd1-8c11-a079efcb23cc">

3. 절대 좌표 (50,50)
<img width="400" alt="image" src="https://github.com/xpile98/SimpleImageCrop/assets/19896491/31bb07ef-2116-4496-aacd-d406606d2f8f">



크롭을 한 후 폴더에 저장된 이미지들을 비교해볼까요?

(전)
<img width="400" alt="image" src="https://github.com/xpile98/SimpleImageCrop/assets/19896491/4f4f0e0a-d524-4c52-812f-bade675bfdd9">


(후)
<img width="400" alt="image" src="https://github.com/xpile98/SimpleImageCrop/assets/19896491/48d093de-4e68-4af4-8a62-e26bb69e23cd">

이미지가 사용자가 원하는 대로 크롭이 되었습니다. 

직관적으로 여러 이미지들을 한번에 크롭할 수 있는 간편한 프로그램이니까 필요하시면 사용해보세요.

문제점이나 개선점 있으면 피드백 부탁드립니다 ^^
