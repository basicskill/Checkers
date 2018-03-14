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

void odredi_stanje(Mat image, vector<vector<char> >& stanje)
{
	for (int i=0; i<6; i++)
		for (int j = 0; j < 6; j++)
		{
			stanje[i][j] = 'n';
		}

	int width = image.cols;
	int height = image.rows;

	Mat g_image;
	cvtColor(image, g_image, cv::COLOR_RGB2GRAY);


	Mat b_image;
	threshold(g_image, b_image, 60, 255, THRESH_BINARY);
	imwrite("bin.jpg", b_image);
	//imshow("jajaj", b_image);


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
	int indexmax=-1;

	//imshow("jajaj", image);

	//cout << contours.size();
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


		//Scalar color = Scalar(0, 255, 0);
		//drawContours(image, approxCurve, i, color, 1, 4, hierarchy, 0, Point());
	}

	//Scalar color = Scalar(0, 255, 0);
	//drawContours(image, approxCurve, indexmax, color, 1, 4, hierarchy, 0, Point());
	//cout << endl <<indexmax;
	//imshow("jajaj", image);
	
	
	Point a, b, c, d;

	if (indexmax < 0) return;

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

	//imshow("jajaj",b_image);
	Mat hsvimage;
	cvtColor(warpedimage, hsvimage, CV_RGB2HSV);
	//imshow("jaja", hsvimage);
	imwrite("warp.jpg", warpedimage);
	imwrite("hsv.jpg", hsvimage);
	
	/*
	Mat temp3 = hsvimage;
	for (int i=0; i<600; i++)
		for (int j=0; j<600; j++) 
		{
			temp3.at<Vec3b>(i, j)[1]=0;
			temp3.at<Vec3b>(i, j)[2]=0;
		}
	imwrite("v.jpg", temp3);
*/

	for (int i = 0; i < 6; i++)
		for (int j = 0; j < 6; j++)
		{
			int sumr = 0, sumb = 0, sumw = 0;

			for (int ii = i * 100; ii<(i + 1) * 100; ii++)
				for (int jj = j * 100; jj < (j + 1) * 100; jj++)
				{
					if ((hsvimage.at<Vec3b>(ii, jj)[0] < 180) &&
						(hsvimage.at<Vec3b>(ii, jj)[1] < 100) &&
						(hsvimage.at<Vec3b>(ii, jj)[2] < 100)) sumb++;

					if ((hsvimage.at<Vec3b>(ii, jj)[0] < 180) &&
						(hsvimage.at<Vec3b>(ii, jj)[1] < 100) &&
						(hsvimage.at<Vec3b>(ii, jj)[2] > 100)) sumw++;

					if ((hsvimage.at<Vec3b>(ii, jj)[0] < 180) &&
						(hsvimage.at<Vec3b>(ii, jj)[1] > 80) &&
						(hsvimage.at<Vec3b>(ii, jj)[2] > 50)) sumr++;
				}

			//cout << sumr << " " << sumb << " " << sumw << endl;
			if (sumr > 5000) stanje.at(i).at(j) = 'r';
			else if (sumb > 5000) stanje.at(i).at(j) = 'b';
			else if (sumw > 5000) stanje.at(i).at(j) = 'w';
			else stanje.at(i).at(j) = 'n';

		}


	/// Show in a window
	//namedWindow("Contours", CV_WINDOW_AUTOSIZE);
	//imshow("Contours", warpedimage);
	//waitKey(0);
	return;
}

int main()
{
	/*
	VideoCapture cap;
	if (!cap.open(0))
	return -1;


	Mat frame;
	cap >> frame;
	*/
	vector<vector<char> > stanje(6, vector<char>(6));

	Mat frame = imread("tabla.png", CV_LOAD_IMAGE_COLOR); ////


	odredi_stanje(frame, stanje);

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


	for (int i = 0; i < 6; i++)
	{
		for (int j = 0; j < 6; j++)
		{
			cout << stanje.at(i).at(j) << " ";
		}
		cout << endl;
	}

	//waitKey(0);
	//system("pause");
	return 0;
}