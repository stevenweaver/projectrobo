#include "opencv/cvaux.h"
#include "opencv/highgui.h"
#include "opencv/cxcore.h"
#include <stdio.h>
 
int main(int argc, char* argv[])
{    
  CvCapture* camera = cvCreateCameraCapture(0); // Use the default camera
 
  IplImage*     frame = 0;
  IplImage      img;
 
  frame = cvQueryFrame(camera); //need to capture at least one extra frame
  frame = cvQueryFrame(camera);
  if (frame != NULL) {
    printf("got frame\n\r");
        cvSaveImage("webcam.jpg", frame);
  } else {
      printf("Null frame\n\r");
  }
  cvReleaseCapture(&camera);
  return 0;
}
