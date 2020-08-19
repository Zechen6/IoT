import numpy as np

# TODO: 无用的骨架点处理，0值的骨架点处理。

class person:
    def __init__(self):
        self.cur_time = 0 # 帧时间记录

        # pose 存储为numpy数组 25x2
        self.cur_pose = None # 存储当前骨架点帧
        self.pre_1_pose = None # 此前一帧骨架点 用于计算速度等
        self.pre_2_pose = None # 此前第两帧骨架点 用于计算加速度等

        self.score = 0 # 评分

        # TODO: all features
        self.features = {
            # 骨架高级特征
            "normalized_pos":[], # 归一化位置
            "cart_track":[], # 笛卡尔的轨迹
            "polar_track":[], # 极坐标轨迹
            "distance":[], # 欧式距离
            "direction":[], # 方向
            "angle":[]
        } # use 字典

    def pose2ndarrary(self,raw_pose):
        '''
        将接收的25x3骨架点转换为25x2的numpy数组
        :param raw_pose: 原始骨架点
        :return: 25x2的numpy数组
        '''
        pose = np.ndarray(raw_pose)
        pose = pose[:,:2] # 舍弃置信度
        return np.ndarray(pose)

    def get_score(self):
        '''
        最后评分
        :return: float, range from [0,100]
        '''
        pass

    def get_xx_features(self, pose):
        '''
        获取单个骨架点的某个某个特征
        :return:
        '''
        pass

    def get_velocity(self):
        '''
        单位时间移动距离作为速度，取2d平面的欧式距离。
        取标量，不计算方向。
        :return:
        '''
        if self.pre_1_pose is not None: # 存在先前状态
            velocity = np.linalg.norm(self.cur_pose - self.pre_1_pose)
            self.features['velocity'] = velocity





    def update(self):
        '''
        当前帧更新
        :return:
        '''
        # 调用全部特征提取
        for feature in self.features:

        self.cur_time += 1

    def save(self,file):
        '''
        保存当前帧时间，提取的特征到txt
        :param file:
        :return:
        '''