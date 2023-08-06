import 'package:flutter/widgets.dart';
import 'package:{{ package_name }}/assembler.dart';

abstract class {{ name }}NavigatorType {

}

class {{ name }}Navigator implements {{ name }}NavigatorType {
  Assembler assembler;

  {{ name }}Navigator({@required this.assembler});
}
