angular.module('safePet')

.controller('mainListController', ['$scope', '$ionicModal', 'userDogsResource','dogsResource','$state','$auth','userInfo', 'Camera', '$http', '$interval', 'lostDogs', 'socketConn', '$cordovaFileTransfer',  '$cordovaImagePicker', function($scope,$ionicModal,userDogsResource,dogsResource,$state,$auth,userInfo,Camera, $http, $interval, lostDogs, socketConn, $cordovaFileTransfer,  $cordovaImagePicker){

    // If the user is not authenticated redirect to the login
    if(!$auth.isAuthenticated()){
        $state.go("login");
    };

    $scope.varI = 1;
    $scope.perfil = 0;
    $scope.myImage = '';
    $scope.myCroppedImage = {};
    //$scope.dogsScanList = {};

    $scope.$watch(function(){return $scope.myCroppedImage}, function(newVal, oldVal){
        $scope.myCroppedImage = newVal;
    });
    // Refresh user information
    userInfo.refresh();
    socketConn.on('changeAccepted', function(){
        userInfo.refresh();
    });
    // Handle User dogs from the API with
    // Event listener: update dog list
    $scope.$on('user:refresh', function(event, data){        
        $scope.dogs = data.dogs;
    });

    // create a new dog when the form is submitted
    $scope.createDog = function(dog) {
        // Add owner id to the dog info
        dog.userId = userInfo.user._id;

        // Save new dog and refreshing dog list in the callback
        dogsResource.save(dog,function(dogReturn){
            //$scope.dogs = userDogsResource.query({id: userInfo.user._id});
            userInfo.refresh();
            $scope.dogModal.hide();
            $scope.dogId = dogReturn._id;        
            //Take photo
            $scope.getPhoto(true);
        });
    };

    // Find all lost dogs.
    $scope.lostdogs = lostDogs.query();
    // Update list on state change
    $scope.$on('dog:lost', function(event, data){
        $scope.lostdogs = lostDogs.query();
    });
    
    
    //Refresh lost dogs on pull
    $scope.doRefresh = function() {
        $http.get('#/app/mainlist')
        .success(function() {
            $scope.lostdogs = lostDogs.query();
        }).finally(function() {
            // Stop the ion-refresher from spinning
            $scope.$broadcast('scroll.refreshComplete');
        });
    };

    // Create and load the Modal
    $ionicModal.fromTemplateUrl('newDog.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.dogModal = modal;
    });
    // Create and load the Modal
    $ionicModal.fromTemplateUrl('newDog2.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.dogModal2 = modal;
    });

    // Open new task modal
    $scope.newDog = function() {
        $scope.dogModal2.hide();
        $scope.dogModal.show();
    };

    $scope.newDog2 = function() {
        $scope.dogModal2.show();
    };

    // Close the new task modal
    $scope.closeNewDog = function() {
        $scope.dogModal.hide();
    };

    $scope.closeNewDog2 = function() {
        $scope.dogModal2.hide();
    };
    // Create and load the Modal Crop
    $ionicModal.fromTemplateUrl('imgCrop.html', function(modal) {
        $scope.cropModal = modal;
    }, {
        scope: $scope,
        animation: 'slide-in-up'
    });

    $ionicModal.fromTemplateUrl('showPhoto.html', function(modal) {
        $scope.showPhoto = modal;
    }, {
        scope: $scope,
        animation: 'slide-in-up'
    });

    $scope.closeShowPhoto = function() {
        $scope.showPhoto.hide();
    };

    $ionicModal.fromTemplateUrl('showScanPhoto.html', function(modal) {
        $scope.showScanPhoto = modal;
    }, {
        scope: $scope,
        animation: 'slide-in-up'
    });

    $scope.closeShowScanPhoto = function() {
        $scope.showScanPhoto.hide();
    };
    $ionicModal.fromTemplateUrl('dogsScan.html', function(modal) {
        $scope.dogsScan = modal;
    }, {
        scope: $scope,
        animation: 'slide-in-up'
    });
     $scope.closeDogsScan = function() {
        $scope.dogsScan.hide();
    };

    $scope.closeShowPhoto = function() {
        $scope.showPhoto.hide();
    }
    // Open new task modal
    $scope.crop = function() {
        $scope.myImage = '';
        $scope.myCroppedImage = '';
        $scope.getPhoto(false);
    };

    // Close the new task modal
    $scope.closeCrop = function() {
        $scope.cropModal.hide();
    };

    //Upload image from galery
    //$scope.collection = [];

    $scope.getImageGalery = function(){
        var options = {
            maximumImagesCount: 1,
            width: 500,
            height: 500,
            quality: 75
        };

        $cordovaImagePicker.getPictures(options).then(function (results) {
            for (var i = 0; i < results.length; i++) {
                console.log('Image URI: ' + results[i]);
                //$scope.collection.push(results[i]);
                $scope.lastPhoto = results[i];
            }
        }, function(error) {
            console.err(err);
        });
    };

    $scope.fileUpload = function (par) {
        if($scope.perfil == 0) {
            var url = "http://safepetapi.labcomp.cl:5000/noseimgs";
            var filename = $scope.dogId + "-" + $scope.varI;
        }
        else {
            alert("Foto de Perfil");
            var url = "http://safepetapi.labcomp.cl:5000/dogsimgs";
            var filename = $scope.dogId;
            $scope.perfil = 0;
            $scope.varI = 10;
        }

        //target path may be local or url
        $scope.dogModal.hide();
        //var filename = targetPath.split("/").pop();
        var targetPath = $scope.lastPhoto;
        var filename = $scope.dogId + "-" + $scope.varI + ".jpg";
        var options = {
            fileKey: "file",
            fileName: filename,
            chunkedMode: false,
            mimeType: "image/jpg"
        };
        if(par){
            $cordovaFileTransfer.upload(url, targetPath, options).then(function(result) {
                alert("¡Imagen Válida!");
                if($scope.varI == 10) {
                    //Profile photo
                    alert("Se ha registrado correctamente");
                    $scope.showPhoto.hide();
                    $scope.varI = 1;
                    $state.go("app.mainlist");
                }
                if($scope.varI == 3){
                    $scope.perfil = 1;
                    $scope.showPhoto.hide();
                    $scope.getPhoto(true);
                } else {
                    $scope.varI++;
                    $scope.showPhoto.hide();
                    $scope.getPhoto(true);
                }
            }, function(err) {
                console.log("ERROR: " + JSON.stringify(err));
                alert("Imagen inválida");
                $scope.varI = 1;
            }, function (progress) {
                // constant progress updates
                $timeout(function () {
                    $scope.downloadProgress = (progress.loaded / progress.total) * 100;
                    })
            });
        } else {
            //scan nose
            $cordovaFileTransfer.upload("http://safepetapi.labcomp.cl:5000/scannose", targetPath, options).then(function(result) {
                alert("¡Imagen Valida!");
                alert(result.response);
                angular.forEach(result.response, function(item){
                    dogsResource.get({id: item}, function(dog){
                        $scope.dogsScanList.push(dog)
                    });
                });
                $scope.showScanPhoto.hide();
                $scope.dogsScan.show();
            });
        }

    };
        /*var options = {
            fileKey: "avatar",
            fileName: "image.png",
            chunkedMode: false,
            mimeType: "image/png"
        };
        socketConn.emit("fileUpload", options);
        socketConn.emit("fileUpload", $scope.lastPhoto);
        $cordovaFileTransfer.upload("http://safepetapi.labcomp.cl:5000/noseimgs", $scope.lastPhoto, options).then(function(result) {
            socketConn.emit("fileUpload", "Success");
            console.log("SUCCESS: " + JSON.stringify(result.response));
        }, function(err) {
            console.log("ERROR: " + JSON.stringify(err));
        }, function (progress) {
            // constant progress updates
        });
        if(par){$scope.dogModal.hide();}
        else{$scope.cropModal.hide();};
    };*/

    $scope.getPhoto = function(opt) {
        console.log('Getting camera');
        Camera.getPicture({
            quality: 75,
            targetWidth: 500,
            targetHeight: 500,
            saveToPhotoAlbum: false
        }).then(function(imageURI){//imageURI) {
            if (opt) {
                $scope.lastPhoto = imageURI;
                $scope.showPhoto.show();
                //imageURI;
                /*var file = $scope.lastPhoto;
                var reader = new FileReader();
                reader.onload = function(e) {
                // Create a new image.
                    var img = new Image();
                // Set the img src property using the data URL.
                    img.src = reader.result;
                // Add the image to the page.
                }
            reader.readAsDataURL(file); 
            alert(reader.readAsDataURL(file));*/
            } else { 
                //Scan Nose
                $scope.lastPhoto = imageURI;
                $scope.showScanPhoto.show();
            };
        }, function(err) {
            console.err(err);
        });
    
        navigator.camera.getPicture(function(imageURI) {
            console.log(imageURI);
        }, function(err) {
        }, { 
            quality: 75,
            destinationType: Camera.DestinationType.DATA_URL//FILE_URI
        });
    };
}]);

