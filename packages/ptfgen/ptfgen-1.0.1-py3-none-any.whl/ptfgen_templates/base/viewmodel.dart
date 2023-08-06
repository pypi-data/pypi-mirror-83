import 'package:flutter/widgets.dart';
import 'package:pt_architecture/pt_architecture.dart';
import 'package:rxdart/rxdart.dart';

import '{{ name_lower }}_navigator.dart';
import '{{ name_lower }}_usecase.dart';

class {{ name }}VMI {
  Stream<void> loadTrigger;

  {{ name }}VMI({@required this.loadTrigger});
}

class {{ name }}VMO {
  Stream<void> loaded;

  {{ name }}VMO({@required this.loaded});
}

class {{ name }}ViewModel implements ViewModelType<{{ name }}VMI, {{ name }}VMO> {
  {{ name }}NavigatorType navigator;
  {{ name }}SceneUseCaseType useCase;

  {{ name }}ViewModel({@required this.navigator, @required this.useCase});

  @override
  {{ name }}VMO transform([{{ name }}VMI input, DisposeBag bag]) {
    Stream<void> loaded = input.loadTrigger;

    return {{ name }}VMO(loaded: loaded);
  }
}
