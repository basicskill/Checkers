#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

int main(int, char**) {
    VideoCapture cap(0); 
    if (!cap.isOpened())
        return -1;
    int br = 0;
    while (true) {
        br += 1;
        Mat frame, frejm1;
        cap.read(frejm1);
        cap >> frame;
        imwrite("slika.jpg", frame);
        imwrite("slidza.jpg", frejm1);
        if (waitKey(30) >= 0) 
            break;
    }
    return 0;
}