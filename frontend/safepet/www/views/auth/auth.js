angular.module('safePet')

.controller('authController', ['$scope','$auth','$state','$ionicModal', '$ionicPopup', 'Camera', function($scope,$auth,$state,$ionicModal,$ionicPopup, Camera){
    $scope.signup = function(user) {
        $auth.signup({
        	displayName: user.displayName,
            email: user.email,
            password: user.password,
            address: user.address,
            phone: user.phone
        })
        .then(function() {
        	$scope.userModal.hide();
            $state.go("app.mainList");
        })
        .catch(function(response) {
        	$ionicPopup.alert({
        	  title: 'Error',
        	  content: response.data ? response.data || response.data.message : response
        	});
        });
    };
    $scope.login = function(user){
        $auth.login({
        	displayName: user.displayName,
            email: user.email,
            password: user.password
        })
        .then(function(){
            $state.go("app.mainList")
        })
        .catch(function(response){
        	$ionicPopup.alert({
        	  title: 'Error',
        	  content: 'Usuario o contraseña incorrectos'//response.data ? response.data || response.data.message : response
        	})
        });
    };

    //Facebook Login
    $scope.authenticate = function(provider) {
      $auth.authenticate(provider)
        .then(function() {
            $state.go("app.mainList")
        })
        .catch(function(response) {
          $ionicPopup.alert({
            title: 'Error',
            content: response.data ? response.data || response.data.message : response
          })

        });
    };

	// Create and load the Modal
	$ionicModal.fromTemplateUrl('newUser.html', function(modal) {
		$scope.userModal = modal;
	}, {
		scope: $scope,
		animation: 'slide-in-up'
	});

	// Open our new task modal
	$scope.newUser = function() {
	  	$scope.userModal.show();
	};

  	// Close the new task modal
	$scope.closeNewUser = function() {
		$scope.userModal.hide();
	};
    // Create and load the Modal Crop
    $ionicModal.fromTemplateUrl('imgCrop.html', function(modal) {
        $scope.cropModal = modal;
    }, {
        scope: $scope,
        animation: 'slide-in-up'
    });

    // Open new task modal
    $scope.crop = function() {
        $scope.myImage = '';
        $scope.myCroppedImage = '';
        $scope.getPhoto();
        //$scope.cropModal.show();
    };

    // Close the new task modal
    $scope.closeCrop = function() {
        $scope.cropModal.hide();
    };


    $scope.getPhoto = function() {
        console.log('Getting camera');
        Camera.getPicture({
        quality: 75,
        targetWidth: 500,
        targetHeight: 500,
        saveToPhotoAlbum: false
        }).then(function(imageURI) {
            //console.log(imageURI);
            $scope.lastPhoto = imageURI;
           /* $scope.showAlert = function() {
        var alertPopup = $ionicPopup.alert({
                title: 'Acerca de SafePet',
                template: '{{lastPhoto}}' 
        });
    };
            $scope.showAlert();*/
            $scope.myImage = imageURI;
            $scope.cropModal.show();

        }, function(err) {
        console.err(err);
    });
    
        navigator.camera.getPicture(function(imageURI) {
            console.log(imageURI);
        }, function(err) {
        }, { 
            quality: 50,
            destinationType: Camera.DestinationType.DATA_URL
        });
    };
}]);