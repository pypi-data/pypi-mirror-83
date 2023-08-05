Model
=====

.. currentmodule:: pykeen.models.base

.. autoclass:: Model
   :show-inheritance:

   .. rubric:: Attributes Summary

   .. autosummary::

      ~Model.can_slice_h
      ~Model.can_slice_r
      ~Model.can_slice_t
      ~Model.loss_default_kwargs
      ~Model.modules_not_supporting_sub_batching
      ~Model.num_entities
      ~Model.num_parameter_bytes
      ~Model.num_relations
      ~Model.regularizer_default_kwargs
      ~Model.supports_subbatching

   .. rubric:: Methods Summary

   .. autosummary::

      ~Model.compute_label_loss
      ~Model.compute_mr_loss
      ~Model.compute_self_adversarial_negative_sampling_loss
      ~Model.get_grad_params
      ~Model.load_state
      ~Model.make_labeled_df
      ~Model.post_parameter_update
      ~Model.predict_heads
      ~Model.predict_scores
      ~Model.predict_scores_all_heads
      ~Model.predict_scores_all_relations
      ~Model.predict_scores_all_tails
      ~Model.predict_tails
      ~Model.regularize_if_necessary
      ~Model.reset_parameters_
      ~Model.save_state
      ~Model.score_all_triples
      ~Model.score_h
      ~Model.score_hrt
      ~Model.score_r
      ~Model.score_t
      ~Model.to_cpu_
      ~Model.to_device_
      ~Model.to_embeddingdb
      ~Model.to_gpu_

   .. rubric:: Attributes Documentation

   .. autoattribute:: can_slice_h
   .. autoattribute:: can_slice_r
   .. autoattribute:: can_slice_t
   .. autoattribute:: loss_default_kwargs
   .. autoattribute:: modules_not_supporting_sub_batching
   .. autoattribute:: num_entities
   .. autoattribute:: num_parameter_bytes
   .. autoattribute:: num_relations
   .. autoattribute:: regularizer_default_kwargs
   .. autoattribute:: supports_subbatching

   .. rubric:: Methods Documentation

   .. automethod:: compute_label_loss
   .. automethod:: compute_mr_loss
   .. automethod:: compute_self_adversarial_negative_sampling_loss
   .. automethod:: get_grad_params
   .. automethod:: load_state
   .. automethod:: make_labeled_df
   .. automethod:: post_parameter_update
   .. automethod:: predict_heads
   .. automethod:: predict_scores
   .. automethod:: predict_scores_all_heads
   .. automethod:: predict_scores_all_relations
   .. automethod:: predict_scores_all_tails
   .. automethod:: predict_tails
   .. automethod:: regularize_if_necessary
   .. automethod:: reset_parameters_
   .. automethod:: save_state
   .. automethod:: score_all_triples
   .. automethod:: score_h
   .. automethod:: score_hrt
   .. automethod:: score_r
   .. automethod:: score_t
   .. automethod:: to_cpu_
   .. automethod:: to_device_
   .. automethod:: to_embeddingdb
   .. automethod:: to_gpu_
