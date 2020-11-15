<?php

header('Content-type: json/application');

require 'controller/connection.php';
require 'controller/functions.php';


$method = $_SERVER['REQUEST_METHOD'];

$q = $_GET['q'];
$params = explode('/', $q);

$type = $params[0];
$id = $params[1];


if ($method === 'GET'){
	if ($type === 'posts'){

		if (isset($id)){
			getPost($connection, $id);
		} else {
			getPosts($connection, $id);
		} 
	} elseif ($type = 'search'){
      getSearch($connection, $id);
  }
} elseif ($method === 'POST'){
	if ($type === 'posts'){
    $data = file_get_contents('php://input');
    $data = json_decode($data, true);
		addPost($connection, $data);
	}
} elseif ($method === 'PATCH') {
  	if($type === 'posts') {
  		if (isset($id)) {
  			$data = file_get_contents('php://input');
  			$data = json_decode($data, true);
  			updatePost($connection, $id, $data);
  		}
  	 }
  } elseif ($method === 'DELETE') {
  		if($type === 'posts') {
  		if (isset($id)) {
  			deletePost($connection, $id);
  		}
  	 }
  }




