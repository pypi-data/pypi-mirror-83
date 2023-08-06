import 'package:flutter/material.dart';
import 'package:pt_architecture/pt_architecture.dart';
import 'package:rxdart/rxdart.dart';

import '{{ name_lower }}_viewmodel.dart';

class {{ name }}View extends StatefulWidget {
  const {{ name }}View({Key key, this.viewModel}) : super(key: key);
  final {{ name }}ViewModel viewModel;

  @override
  _{{ name }}ViewState createState() => _{{ name }}ViewState();
}

class _{{ name }}ViewState extends State<{{ name }}View> with DisposeBagMixin, Bindable {
  /// Properties

  {{ name }}VMO output;

  /// Subjects
  
  var loadTrigger = PublishSubject<void>();

  /// Life Cycle

  @override
  void bindViewModel() {
    final input = {{ name }}VMI(
      loadTrigger: Stream<void>.value(null),
    );
    output = widget.viewModel.transform(input, bag);
    output.loaded.listen(null);
  }

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(),
    );
  }
}

/// Build Methods
extension {{ name }}BuildMethods on _{{ name }}ViewState {
  // Widget _buildSomething() {
  //   return Container(
  //     child: StreamBuilder<void>(
  //         stream: output.something,
  //         builder: (context, snapshot) {
  //           return Container();
  //         }),
  //   );
  // }
}

