angular.module('safePet')

.controller('dogDetailsController', ['$scope', 'dogsResource','$stateParams','$state','$ionicModal', 'userInfo', '$rootScope', '$ionicPopup', 'socketConn', 'usersResource', function($scope,dogsResource,$stateParams,$state,$ionicModal, userInfo, $rootScope, $ionicPopup, socketConn, usersResource){

	$scope.UserId = userInfo.userId;
    $scope.dog = dogsResource.get({id: $stateParams.dogId}, function(d){
        usersResource.get({id: d.owner}, function(usr){
            $scope.owner = usr.displayName;
        });
    });
	
    $scope.editDogProfile = function(dog){
        dogsResource.update({id: $scope.dog._id},{data: $scope.dog});
        $scope.editDogModal.hide();
    };

	$scope.reportLostDog = function () {
		if($scope.dog.lost)
		{
			dogsResource.update({id: $stateParams.dogId},{data: {lost: 0}},function(){
				$scope.dog = dogsResource.get({id: $stateParams.dogId}, function(){
                    $rootScope.$broadcast('dog:lost', 'Mis datos');
                });
				$scope.closeFoundDog();
				$scope.closeLostDog();
                $state.go('app.mainList')
			});

		}else{
			dogsResource.update({id: $stateParams.dogId},{data: {lost: 1}},function(){
				$scope.dog = dogsResource.get({id: $stateParams.dogId}, function(){
                    $rootScope.$broadcast('dog:lost', 'Mis datos');
                    socketConn.emit("reportLostDog", {userId: userInfo.userId});
                });
				$scope.closeFoundDog();
				$scope.closeLostDog();
                $state.go('app.mainList')
			});
		}
	};

    // Create and load the edit dog Modal
    $ionicModal.fromTemplateUrl('editDog.html', function(modal) {
        $scope.editDogModal = modal;
    }, {
        scope: $scope,
        animation: 'slide-in-up'
    });
    // Open edit dog modal
    $scope.editDog = function() {
        $scope.editDogModal.show();
    };
    //Close edit dog modal
    $scope.closeEditDog = function() {
        $scope.editDogModal.hide();
    };

    //Go to change owner
    $scope.change = function() {
        $scope.editDogModal.hide();
        $state.go('app.change', {"dogId": $stateParams.dogId});
    };
	// Create and load the lost dog Modal
    $ionicModal.fromTemplateUrl('lostDog.html', function(modal) {
        $scope.lostDogModal = modal;
    }, {
        scope: $scope,
        animation: 'slide-in-up'
    });

    // Open new task modal
    $scope.lostDog = function() {
        $scope.lostDogModal.show();
    };

    // Close the new task modal
    $scope.closeLostDog = function() {
        $scope.lostDogModal.hide();
    };

	// Create and load the found dog Modal
    $ionicModal.fromTemplateUrl('foundDog.html', function(modal) {
        $scope.foundDogModal = modal;
    }, {
        scope: $scope,
        animation: 'slide-in-up'
    });

    // Open new task modal
    $scope.foundDog = function() {
        $scope.foundDogModal.show();
    };

    // Close the new task modal
    $scope.closeFoundDog = function() {
        $scope.foundDogModal.hide();
    };

    $scope.confirmDogDelete = function(){
        var deleteConfirm = $ionicPopup.confirm({
            title: "Eliminar Perro",
            template: "¿Está seguro que quiere eliminar a su perro? Borrarlo es un proceso irreversible"
        }).then(function(res){
            if(res){
                dogsResource.delete({id: $stateParams.dogId},
                    function(value, responseHeaders){
                        $scope.editDogModal.hide();
                        userInfo.refresh();
                        $state.go('app.mainList');
                    },
                    function(httpResponse){
                        $ionicPopup.alert({
                            title: "Error",
                            template: "No se ha podido eliminar su mascota. Inténtelo más tarde"
                        });
                    }
                );
            } 
        });
    };
}]);