import numpy as np
import tensorflow as tf
import input_data
import model
import cv2
import os


#%% Evaluate one image
#when training, comment the following codes.





def evaluate_one_image():
   '''Test one image against the saved models and parameters
   '''

   # you need to change the directories to yours.
   N_CLASSES = 2
   IMG_W = 100  # resize the image, if the input image is too large, training will be very slow.
   IMG_H = 100
   BATCH_SIZE = 200
   CAPACITY = 200
   MAX_STEP = 1  # with current parameters, it is suggested to use MAX_STEP>10k
   learning_rate = 0.0001
   train_dir = 'D:\shipdetection\\test200' #测试 50%
   #train_dir = 'D:\shipdetection\data' #训练集
   logs_train_dir = 'D:\shipdetection\gf3log2'

   train, train_label = input_data.get_files(train_dir)
   train_batch, train_label_batch = input_data.get_batch(train,
                                                         train_label,
                                                         IMG_W,
                                                         IMG_H,
                                                         BATCH_SIZE,
                                                         CAPACITY)

   train_logits = model.inference(train_batch, BATCH_SIZE, N_CLASSES)
  #   #  # 打印 预测与真实标签
  #  with tf.Session() as sess:
  #       print("train_logits:%s"%sess.run(train_logits))
  #       print("\n")
  #       print("label:%s"%sess.run(train_label_batch))
  # # 打印 预测与真实标签 主要为了求召回率精确度
   train_logits= tf.nn.softmax(train_logits) # model.infrence 中最后一层未使用softmax 所以在这里要使用
   train__acc = model.evaluation(train_logits, train_label_batch)

   sess = tf.Session()

   saver = tf.train.Saver() #
   ckpt = tf.train.get_checkpoint_state(logs_train_dir)
   print(ckpt)
   if ckpt and ckpt.model_checkpoint_path:
       global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
       #saver.restore(sess, ckpt.model_checkpoint_path)
       #  不同迭代次数精度
       path='D:\shipdetection\gf3log2\model.ckpt-7999'
       saver.restore(sess, path)
       #  不同迭代次数精度
       print('Loading success, global_step is %s' % global_step)
   else:
       print('No checkpoint file found')

   coord = tf.train.Coordinator()
   threads = tf.train.start_queue_runners(sess=sess, coord=coord)

   try:
       for step in np.arange(MAX_STEP):
           if coord.should_stop():
               break


           tra_acc = sess.run(train__acc)

           # print("train_logits:%s" %train_logits.eval(session=sess))
           # print("\n")
           # print("label:%s" % train_label_batch.eval(session=sess))



           print('Step %d, train accuracy = %.2f%%' % (step,  tra_acc * 100.0))




   except tf.errors.OutOfRangeError:
       print('Done training -- epoch limit reached')
   finally:
       coord.request_stop()

   coord.join(threads)
   sess.close()







evaluate_one_image()
