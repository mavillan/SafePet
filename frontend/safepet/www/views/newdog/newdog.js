angular.module('safePet')

.controller('newDogController', ['$scope', '$ionicModal', 'Upload', 'userInfo','Camera', '$cordovaFileTransfer', 'dogsResource', '$state','confirmDog', 'confirmNose', '$cordovaImagePicker', function($scope, $ionicModal, Upload, userInfo, Camera, $cordovaFileTransfer, dogsResource, $state, confirmNose, confirmDog, $cordovaImagePicker){
	//Verifiers
	$scope.nose1 = 0;
	$scope.nose2 = 0;
	$scope.nose3 = 0;
	$scope.perfil = 0;
	//Modals
	$ionicModal.fromTemplateUrl('nose1.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.nose1modal = modal;
    });
    //
	$ionicModal.fromTemplateUrl('nose2.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.nose2modal = modal;
    });
    //
	$ionicModal.fromTemplateUrl('nose3.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.nose3modal = modal;
    });
    //
	$ionicModal.fromTemplateUrl('perfil.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.perfilmodal = modal;
    });
    //Handle if getImageGalery or getPhoto
    /*$scope.selectType = function(opt){

    }*/
    //Get Photo from gallery
    $scope.getImageGalery = function(opt){
        var options = {
            maximumImagesCount: 1,
            width: 500,
            height: 500,
            quality: 100
        };

        $cordovaImagePicker.getPictures(options).then(function (results) {
            for (var i = 0; i < results.length; i++) {
                console.log('Image URI: ' + results[i]);
                //$scope.collection.push(results[i]);
                $scope.picFile = results[i];
	            if(opt == 1){
	            	$scope.nose1modal.show();	
	            } else if(opt == 2) {
	        		$scope.nose2modal.show();	
	            } else if(opt == 3) {
	            	$scope.nose3modal.show();
	            } else {
	            	$scope.perfilmodal.show();
	            }
            }
        }, function(error) {
            console.err(err);
        });
    };

    // -------------------
    //Get Photo Function
    $scope.getPhoto = function(opt) {
        console.log('Getting camera');
        Camera.getPicture({
            quality: 100,
            targetWidth: 500,
            targetHeight: 500,
            saveToPhotoAlbum: false
        }).then(function(imageURI){
            $scope.picFile = imageURI;
            if(opt == 1){
            	$scope.nose1modal.show();	
            } else if(opt == 2) {
        		$scope.nose2modal.show();	
            } else if(opt == 3) {
            	$scope.nose3modal.show();
            } else {
            	$scope.perfilmodal.show();
            }
        }, function(err) {
            console.err(err);
        });
    
        navigator.camera.getPicture(function(imageURI) {
            console.log(imageURI);
        }, function(err) {
        }, { 
            quality: 100,
            destinationType: Camera.DestinationType.DATA_URL
        });
    };

    //File Upload
    $scope.upload = function (photo, nose, num) {
        if(nose) {
            var url = "http://safepetapi.labcomp.cl:5000/noseimgs";
            var filename = userInfo.userId + "_registro-" + num + ".jpg";
        }
        else {
            var url = "http://safepetapi.labcomp.cl:5000/dogsimgs";
            var filename = userInfo.userId + "_registro.jpg";
        }

        var targetPath = $scope.picFile;
        var options = {
            fileKey: "file",
            fileName: filename,
            chunkedMode: false,
            mimeType: "image/jpg"
        };       
		$cordovaFileTransfer.upload(url, targetPath, options).then(function(result) {
			if(nose){
				alert("¡Imagen Válida!");
			}            
            if(num == 1){
            	$scope.nose1 = 1;
            	$scope.nose1modal.hide();	
            } else if(num == 2) {
            	$scope.nose2 = 1;
        		$scope.nose2modal.hide();	
            } else if(num == 3) {
            	$scope.nose3 = 1;
            	$scope.nose3modal.hide();
            } else {
            	$scope.perfil = 1;
            	$scope.perfilmodal.hide();
            }
       	}, function(err) {
            console.log("ERROR: " + JSON.stringify(err));
            alert("Imagen inválida");
        });
    };
   
    // create a new dog when the form is submitted
    $scope.createDog = function(dog) {
        // Add owner id to the dog info
        dog.userId = userInfo.user._id;

        // Save new dog and refreshing dog list in the callback
        dogsResource.save(dog,function(dogReturn){            
            userInfo.refresh();
            confirmNose.save({userId: dog.userId, dogId: dogReturn._id});
            confirmDog.save({userId: dog.userId, dogId: dogReturn._id});
            alert("Se ha registrado con éxito");

            $state.go("app.mainList");
        });
    };
}]);