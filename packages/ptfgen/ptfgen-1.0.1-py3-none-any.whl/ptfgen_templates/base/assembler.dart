import 'package:{{ package_name }}/mock/{{ name_lower }}_usecase_mock.dart';

import '{{ name_lower }}_navigator.dart';
import '{{ name_lower }}_usecase.dart';
import '{{ name_lower }}_view.dart';
import '{{ name_lower }}_viewmodel.dart';

class {{ name }}Assembler {
  {{ name }}View resolve{{ name }}View() {
    return {{ name }}View(viewModel: resolve{{ name }}ViewModel());
  }

  {{ name }}ViewModel resolve{{ name }}ViewModel() {
    return {{ name }}ViewModel(navigator: resolve{{ name }}Navigator(), useCase: resolve{{ name }}SceneUseCase());
  }

  {{ name }}NavigatorType resolve{{ name }}Navigator() {
    return {{ name }}Navigator(assembler: this);
  }

  {{ name }}SceneUseCaseType resolve{{ name }}SceneUseCase() {
    return true ? {{ name }}SceneUseCase() : {{ name }}SceneUseCaseMock();
  }
}
