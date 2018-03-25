#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/imgcodecs/imgcodecs.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <vector>
#include <stdlib.h>
#include <stdio.h>

using namespace std;
using namespace cv;
void odredi_stanje(Mat image, vector<vector<char> >& stanje, int bind, int binc, int wv, int ws, int bv)
{
	for (int i = 0; i<6; i++)
		for (int j = 0; j < 6; j++)
		{
			stanje[i][j] = 'n';
		}

	int width = image.cols;
	int height = image.rows;

	Mat g_image;
	cvtColor(image, g_image, cv::COLOR_RGB2GRAY);


	Mat b_image;
	adaptiveThreshold(g_image, b_image, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, bind, binc);
	
	
	int dim2 = 5, dim3 = 3;
	Mat kernel2(dim2, dim2, DataType<int>::type);
	for (int i = 0; i < dim2; i++)
		for (int j = 0; j < dim2; j++) kernel2.at<int>(i, j) = 1;
	Mat kernel3(dim3, dim3, DataType<int>::type);
	for (int i = 0; i < dim3; i++)
		for (int j = 0; j < dim3; j++) kernel3.at<int>(i, j) = 1;


	erode(b_image, b_image, kernel2);
	//dilate(b_image, b_image, kernel3);
	//dilate(b_image, b_image, kernel2);
	//dilate(b_image, b_image, kernel2);
	

	imwrite("bin.jpg", b_image);

	Mat filled_image = b_image.clone();
	floodFill(filled_image, Point(0, 0), Scalar(0));
	bitwise_not(filled_image, filled_image);
	Mat b_filled_image = (filled_image & b_image);

	int dim = 15;
	Mat kernel(dim, dim, DataType<int>::type);
	for (int i = 0; i < dim; i++)
		for (int j = 0; j < dim; j++) kernel.at<int>(i, j) = 1;


	dilate(b_filled_image, b_filled_image, kernel);
	erode(b_filled_image, b_filled_image, kernel);
	bitwise_not(b_filled_image, b_filled_image);

	vector<vector<Point> > contours;
	vector<Vec4i> hierarchy;
	findContours(b_filled_image, contours, hierarchy, CV_CHAIN_APPROX_SIMPLE, CV_CHAIN_APPROX_NONE);

	vector<vector<Point> > approxCurve(contours.size());
	double epsilon = 15;
	double max = 0;
	int indexmax = -1;

	Mat drawing = Mat::zeros(b_image.size(), CV_8UC3);
	for (int i = 0; i < contours.size(); i++)
	{
		approxPolyDP(contours.at(i), approxCurve.at(i), epsilon, true);

		if (approxCurve.at(i).size() == 4)
		{
			double area = contourArea(approxCurve.at(i));
			if (area > max)
			{
				max = area;
				indexmax = i;
			}
		}
	}

	if (indexmax < 0) return;

	//Scalar color = Scalar(0, 255, 0);
	//drawContours(image, approxCurve, indexmax, color, 1, 4, hierarchy, 0, Point());
	

	Point a, b, c, d;

	double minim = (approxCurve.at(indexmax).at(0).x ^ 2) + (approxCurve.at(indexmax).at(0).y ^ 2);
	int minimindex = 0;
	for (int i = 1; i < 4; i++)
	{
		if ((approxCurve.at(indexmax).at(i).x ^ 2) + (approxCurve.at(indexmax).at(i).y ^ 2) < minim)
		{
			minim = (approxCurve.at(indexmax).at(i).x ^ 2) + (approxCurve.at(indexmax).at(i).y ^ 2);
			minimindex = i;
		}
	}
	a = approxCurve.at(indexmax).at(minimindex);

	minim = ((image.cols - approxCurve.at(indexmax).at(0).x) ^ 2) + (approxCurve.at(indexmax).at(0).y ^ 2);
	minimindex = 0;
	for (int i = 1; i < 4; i++)
	{
		if (((image.cols - approxCurve.at(indexmax).at(i).x) ^ 2) + (approxCurve.at(indexmax).at(i).y ^ 2) < minim)
		{
			minim = ((image.cols - approxCurve.at(indexmax).at(i).x) ^ 2) + (approxCurve.at(indexmax).at(i).y ^ 2);
			minimindex = i;
		}
	}
	b = approxCurve.at(indexmax).at(minimindex);

	minim = (approxCurve.at(indexmax).at(0).x ^ 2) + ((image.rows - approxCurve.at(indexmax).at(0).y) ^ 2);
	minimindex = 0;
	for (int i = 1; i < 4; i++)
	{
		if ((approxCurve.at(indexmax).at(i).x ^ 2) + ((image.rows - approxCurve.at(indexmax).at(i).y) ^ 2) < minim)
		{
			minim = (approxCurve.at(indexmax).at(i).x ^ 2) + ((image.rows - approxCurve.at(indexmax).at(i).y) ^ 2);
			minimindex = i;
		}
	}

	c = approxCurve.at(indexmax).at(minimindex);

	minim = ((image.cols - approxCurve.at(indexmax).at(0).x) ^ 2) + ((image.rows - approxCurve.at(indexmax).at(0).y) ^ 2);
	minimindex = 0;
	for (int i = 1; i < 4; i++)
	{
		if (((image.cols - approxCurve.at(indexmax).at(i).x) ^ 2) + ((image.rows - approxCurve.at(indexmax).at(i).y) ^ 2) < minim)
		{
			minim = ((image.cols - approxCurve.at(indexmax).at(i).x) ^ 2) + ((image.rows - approxCurve.at(indexmax).at(i).y) ^ 2);
			minimindex = i;
		}
	}
	d = approxCurve.at(indexmax).at(minimindex);

	vector<Point> points1(4), points2(4);

	points1.at(0) = a;
	points1.at(1) = b;
	points1.at(2) = c;
	points1.at(3) = d;

	points2.at(0) = Point(0, 0);
	points2.at(1) = Point(600, 0);
	points2.at(2) = Point(0, 600);
	points2.at(3) = Point(600, 600);

	Mat H = findHomography(Mat(points1), Mat(points2));

	Mat warpedimage(600, 600, CV_8UC3);
	warpPerspective(image, warpedimage, H, warpedimage.size());


	int minc = 255, maxc = 0;
	for (int i = 0; i<600; i++)
		for (int j = 0; j < 600; j++)
		{
			if (warpedimage.at<Vec3b>(i, j)[0] < minc) minc = warpedimage.at<Vec3b>(i, j)[0];
			if (warpedimage.at<Vec3b>(i, j)[0] > maxc) maxc = warpedimage.at<Vec3b>(i, j)[0];
			if (warpedimage.at<Vec3b>(i, j)[1] < minc) minc = warpedimage.at<Vec3b>(i, j)[1];
			if (warpedimage.at<Vec3b>(i, j)[1] > maxc) maxc = warpedimage.at<Vec3b>(i, j)[1];
			if (warpedimage.at<Vec3b>(i, j)[2] < minc) minc = warpedimage.at<Vec3b>(i, j)[2];
			if (warpedimage.at<Vec3b>(i, j)[2] > maxc) maxc = warpedimage.at<Vec3b>(i, j)[2];
		}
	for (int i = 0; i<600; i++)
		for (int j = 0; j < 600; j++)
		{
			warpedimage.at<Vec3b>(i, j)[0] = 255 * (warpedimage.at<Vec3b>(i, j)[0] - minc) / (maxc - minc);
			warpedimage.at<Vec3b>(i, j)[1] = 255 * (warpedimage.at<Vec3b>(i, j)[1] - minc) / (maxc - minc);
			warpedimage.at<Vec3b>(i, j)[2] = 255 * (warpedimage.at<Vec3b>(i, j)[2] - minc) / (maxc - minc);
		}


	Mat hsvimage;
	cvtColor(warpedimage, hsvimage, CV_RGB2HSV);
	imwrite("warp.jpg", warpedimage);
	imwrite("hsv.jpg", hsvimage);

	
	for (int i = 0; i < 6; i++)
		for (int j = 0; j < 6; j++)
		{
			int sumr = 0, sumb = 0, sumw = 0;

			for (int ii = i * 100; ii<(i + 1) * 100; ii++)
				for (int jj = j * 100; jj < (j + 1) * 100; jj++)
				{
					if ((hsvimage.at<Vec3b>(ii, jj)[0] < 180) &&
						(hsvimage.at<Vec3b>(ii, jj)[1] < 255) &&
						(hsvimage.at<Vec3b>(ii, jj)[2] < bv)) sumb++;

					else if ((hsvimage.at<Vec3b>(ii, jj)[0] < 180) &&
						(hsvimage.at<Vec3b>(ii, jj)[1] < ws) &&
						(hsvimage.at<Vec3b>(ii, jj)[2] > wv)) sumw++;

					else sumr++;
					/*if ((hsvimage.at<Vec3b>(ii, jj)[0] < 180) &&
						(hsvimage.at<Vec3b>(ii, jj)[1] > reds) &&
						(hsvimage.at<Vec3b>(ii, jj)[2] > redv)) sumr++;
					*/
				}

			//cout << sumr << " " << sumb << " " << sumw << endl;
			if (sumb > 5000) stanje.at(i).at(j) = 'b';
			else if (sumw > 5000) stanje.at(i).at(j) = 'w';
			else if (sumr > 5000) stanje.at(i).at(j) = 'r';
			else stanje.at(i).at(j) = 'n';

		}


	/// Show in a window
	//namedWindow("Contours", CV_WINDOW_AUTOSIZE);
	//imshow("Contours", warpedimage);
	//waitKey(0);
	return;
}


int main (int argc, char *argv[])
{
	/*
	VideoCapture cap;
	if (!cap.open(0))
	return -1;


	Mat frame;
	cap >> frame;
	*/
	int bind = atoi(argv[1]);
	int binc = atoi(argv[1]);
	int wv = atoi(argv[2]);
	int ws = atoi(argv[3]);
	int bv = atoi(argv[4]);


	vector<vector<char> > stanje(6, vector<char>(6));

	Mat frame = imread("tabla.jpg", CV_LOAD_IMAGE_COLOR); ////


	odredi_stanje(frame, stanje, bind, binc, wv, ws, bv);

	for (int i = 0; i < 6; i++)
	{
		for (int j = 0; j < 6; j++)
		{
			cout << stanje.at(i).at(j) << "";
		}
		//cout << endl;
	} // !!!!!!!!!!!!!!!!!!!!!!!!11 dole
	for (int i = 0; i < 6; i++)
	{
		for (int j = 0; j < 6; j++)
		{
			if (stanje.at(i).at(j) == 'n')
			{
				cout << -1;
				//system("pause");
				return 0;
			}
		}
	}



	//waitKey(0);
	//system("pause");
	return 0;
}