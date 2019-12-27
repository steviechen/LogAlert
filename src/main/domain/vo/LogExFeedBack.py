class Feedback(object):
    def __init__(self,feedback):
        self.feedback:list[SingleResult] = feedback


class SingleResult(object):
    def __init__(self,component,server_type,predict_label,tracking_id,target_tracking_id):
        self.component = component
        self.server_type = server_type
        self.predict_label = predict_label
        self.tracking_id = tracking_id
        self.target_tracking_id = target_tracking_id