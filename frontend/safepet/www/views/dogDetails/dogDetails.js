angular.module('safePet')

.controller('dogDetailsController', ['$scope', 'dogsResource','$stateParams','$state','$ionicModal', function($scope,dogsResource,$stateParams,$state,$ionicModal){

	$scope.dog = dogsResource.get({id: $stateParams.dogId});

	$scope.deleteDog = function () {
		dogsResource.delete({id: $stateParams.dogId});
		
		$state.go('app.mainList');
	};

	$scope.reportLostDog = function () {
		if($scope.dog.lost)
		{
			dogsResource.update({id: $stateParams.dogId},{data: {lost: 0}},function(){
				$scope.dog = dogsResource.get({id: $stateParams.dogId});
				$scope.closeFoundDog();
				$scope.closeLostDog();
			});

		}else{
			dogsResource.update({id: $stateParams.dogId},{data: {lost: 1}},function(){
				$scope.dog = dogsResource.get({id: $stateParams.dogId});
				$scope.closeFoundDog();
				$scope.closeLostDog();
			});
		}
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
}]);
