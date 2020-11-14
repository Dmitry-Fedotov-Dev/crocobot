<?php 

 function getPosts ($connection) {

 		$posts = mysqli_query($connection, "SELECT * FROM json_table");
		$postsList = [];
		while ($post = mysqli_fetch_assoc($posts)) {
			$postsList[] = $post;
		}
		echo json_encode($postsList);

 }

 function getPost ($connection, $id){
 		$post = mysqli_query($connection, "SELECT * FROM json_table WHERE id = '$id'");
 		if (mysqli_num_rows($post) === 0){

 			http_response_code(404);
 			$res = [
 					"status" => false,
 					"message" => "Post not found"
 			];
 			echo json_encode($res);

 		} else{
 			$post = mysqli_fetch_assoc($post);
 			echo json_encode($post);
 		}
 		
 }


 function addPost($connection, $data) {
 	if (count($data) == 1){
 	//	$data = $data[0];
 	//	echo var_dump($data);
 		$title = $data['товар'];
	 	$made_by = $data['завод'];
	 	$code = $data['код'];
	 	$price = $data['цена'];
	 	mysqli_query($connection, "INSERT INTO `json_table2` (`id`, `название`, `производитель`, `код`, `цена`) VALUES (NULL, '$title', '$made_by', '$code','$price')");

	 	http_response_code(201);
	 	$res = [
	 			"status" => true,
	 			"post_id" => mysqli_insert_id($connection)
	 			 ];
	 	echo json_encode($res);
 		} elseif (count($data) > 1){
 			foreach ($data as $value){
 				$title = $value['товар'];
			 	$made_by = $value['завод'];
			 	$code = $value['код'];
			 	$price = $value['цена'];
			 	mysqli_query($connection, "INSERT INTO `json_table2` (`id`, `название`, `производитель`, `код`, `цена`) VALUES (NULL, '$title', '$made_by', '$code','$price')");
 			}
	 		http_response_code(201);
		 	$res = [
		 			"status" => true,
		 			"post_id" => mysqli_insert_id($connection)
		 			 ];
		 	echo json_encode($res);
 		}else{
 			echo 'JSON is empty.';

 		}
 	}
 	


 function updatePost ($connection, $id, $data) {
 		$title = $data['title'];
 		$body = $data['body'];
 		mysqli_query($connection, " UPDATE json_table SET title = '$title', body = '$body' WHERE json_table.id = '$id' ");

 		http_response_code(200);
 		$res = [
 					"status" => true,
 					"message" => "Post is updated"
 				];

 		echo json_encode($res);
 }

 function deletePost($connection, $id){
 	mysqli_query($connection, " DELETE FROM json_table WHERE json_table.id = '$id' ");

 	http_response_code(200);
 		$res = [
 					"status" => true,
 					"message" => "Post is deleted"
 				];

 		echo json_encode($res);


 }