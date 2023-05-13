import 'package:dio/dio.dart';
import 'package:flutter/material.dart';

const String baseUrl = 'https://<enter_server_address_here>/translate';

class DioUploadService {
  Future<String> uploadImage(String imagePath, BuildContext context) async {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Please wait'),
          content: const Text('Uploading image...'),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('OK'),
            ),
          ],
        );
      },
    );
    Dio dio = Dio();

    FormData formData = FormData.fromMap({
      'image': await MultipartFile.fromFile(imagePath, filename: 'image.jpg'),
    });
    try {
      Response response = await dio.post(
        baseUrl,
        data: formData,
      );
      Navigator.of(context).pop();
      print(response.data);
      return response.toString();
    } catch (e) {
      return 'there was an error';
    }
  }
}
