def calculate_iou(box1, box2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.
    """
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = box1_area + box2_area - inter_area

    return inter_area / union_area if union_area != 0 else 0

def filter_text_blocks(text_blocks, iou_threshold=0.5, area_threshold=0.5, score_threshold=0.5):
    """
    Filter overlapping TextBlocks based on Intersection over Union (IoU),
    area ratio, and score thresholds.
    """
    optimized_blocks = []
    for i, block1 in enumerate(text_blocks):
        keep = True
        for j, block2 in enumerate(text_blocks):
            if i != j:
                box1 = [block1.block.x_1, block1.block.y_1, block1.block.x_2, block1.block.y_2]
                box2 = [block2.block.x_1, block2.block.y_1, block2.block.x_2, block2.block.y_2]
                iou = calculate_iou(box1, box2)

                if iou > iou_threshold:
                    inter_area = iou * (box1[2] - box1[0]) * (box1[3] - box1[1])
                    if inter_area / ((box1[2] - box1[0]) * (box1[3] - box1[1])) > area_threshold or inter_area / ((box2[2] - box2[0]) * (box2[3] - box2[1])) > area_threshold:
                        keep = False
                        break
                    if block1.score < score_threshold and block2.score < score_threshold:
                        keep = False
                        break
                    if block1.score < block2.score:
                        keep = False
                        break
        if keep:
            optimized_blocks.append(block1)

    return optimized_blocks
