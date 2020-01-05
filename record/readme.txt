2019.12.31
	第一代算法主要通过灰度化->中值模糊->Canny边缘检测->霍夫变换道路->最小二乘法拟合 来实现的
	figure11~figure14 是该算法的一些成果
	wrong11~wrong15 是该算法的一些不足
		wrong11、12、14、15 主要是算法不仅仅检测到直线，还检测到环境中除道路以外的东西
		wrong13 说明了用斜率来判断左右车道的一些不足之处
2020.1.5
	优化了算法，添加霍夫变换后对直线的筛选
	该算法在对实际车道图像（/test/RealRoad下存在问题）
		image3: 车道存在阴影部分
		image4: 无法识别短的、虚线车道
		image5: 道路存在水渍
		image8: 存在电线杆阴影、虚线车道相比于image4大
		image10: 草地状况复杂
		image14: 道路上的阴影阳光导致复杂
		image17: 同image4
		image19：同上
		image21: 没有确定的右车道
		image23: 同上
		image25: 同上
		image26: 复杂且没有明确右车道
		image27: 同image4
		image34: 路况复杂
		image35: 道路弯曲
		image38: 右车道模糊
		image46: 路况复杂
		image47: 遇到闸口
		image51：检测不到右车道且存在花纹


